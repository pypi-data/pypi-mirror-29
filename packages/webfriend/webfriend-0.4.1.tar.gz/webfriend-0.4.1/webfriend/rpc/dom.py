from __future__ import absolute_import
from __future__ import unicode_literals
from webfriend.rpc import Base
import logging
import math
import re
import time
from webfriend import exceptions

RX_ID_EXPANSION = re.compile('#(?P<id>[^\s]+)')


class NoSuchElement(Exception):
    pass


class InvalidElement(Exception):
    pass


class DOMElement(object):
    def __init__(self, rpc, definition):
        self.dom = rpc
        self.populate(definition)

    def populate(self, definition):
        if not isinstance(definition, dict):
            raise AttributeError("DOM Element definition must be a dict")

        if 'nodeId' not in definition or definition['nodeId'] is None:
            raise AttributeError("DOM Element definition must contain 'nodeId'")

        if 'nodeName' not in definition:
            self._partial = True
        else:
            self._partial = False

        self.definition  = definition
        self.id          = definition['nodeId']
        self.parent_id   = definition.get('parentId')
        self.type        = definition.get('nodeType')
        self.local_name  = definition.get('localName')
        self.attributes  = {}
        self._box_model  = None
        self._name       = definition.get('nodeName')
        self._value      = definition.get('nodeValue')
        self.child_nodes = []
        self._text       = ''
        self.child_ids   = set()
        self._bounding_rect = None

        # populate children
        if len(definition.get('children', [])):
            for child in definition['children']:
                child_type = child.get('nodeType')

                if child_type == 1:
                    self.child_ids.add(child['nodeId'])

                elif child_type == 3:
                    self._text = child.get('nodeValue', '')

                else:
                    self.child_nodes.append(DOMElement(self.dom, child))

        # populate attributes
        if len(definition.get('attributes', [])):
            attrgen = (a for a in definition['attributes'])

            for name, value in [(n, attrgen.next()) for n in attrgen]:
                self.attributes[name] = value

    def evaluate(self, script, return_by_value=False, own_properties=False, accessors_only=True):
        remote_object = self.dom.call('resolveNode', nodeId=self.id).result.get('object', {})
        object_id = remote_object['objectId']

        # retrieve details via script injection
        try:
            # call the function to retrieve runtime position info
            result = self.dom.tab.runtime.call_function_on(
                object_id,
                "function(){{ {} }}".format(script),
                return_by_value=return_by_value,
            ).result.get('result')

            # if we asked to return the value, then do so now
            if return_by_value:
                return result

            result_id = result.get('objectId')

            if result_id:
                # retrieve the object that resulted from that call
                properties = self.dom.tab.runtime.get_properties(
                    result_id,
                    own_properties=own_properties,
                    accessors_only=accessors_only
                )

                # release that object
                self.dom.tab.runtime.release_object(result_id)
            else:
                properties = []

            # return the data
            return dict([
                (p['name'], p.get('value', {}).get('value')) for p in properties if not p['name'].startswith('_')
            ])

        finally:
            if not return_by_value:
                self.dom.tab.runtime.release_object(object_id)

    def click(self, ensure_target=True, scroll_to=True):
        if self.attributes.get('target') == '_blank':
            del self['target']

        # if specified, scroll down to the element if it's below the fold
        if scroll_to:
            if self.top > self.dom.root.height:
                self.scroll_to()

        return self.evaluate("return this.click()", return_by_value=True)

    def scroll_to(self, x=None, y=None):
        if x is None:
            x = 0

        if y is None:
            y = self.top

        return self.evaluate(
            "window.scrollTo({}, {})".format(x, y),
            return_by_value=True
        )

    @property
    def is_partial(self):
        return self._partial

    @property
    def name(self):
        return self._name

    # @name.setter
    # def name(self, v):
    #     response = self.dom.call('setNodeName', nodeId=self.id, name='{}'.format(v))
    #     return response.get('params', {})['nodeId']

    @property
    def content_document(self):
        if isinstance(self.definition.get('contentDocument'), dict):
            if 'nodeId' in self.definition['contentDocument']:
                return DOMElement(self.dom, self.definition['contentDocument'])

        return None

    @property
    def text(self):
        return self._text

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.dom.call('setNodeValue', nodeId=self.id, value='{}'.format(v))

    @property
    def outer_html(self):
        return self.dom.call('getOuterHTML', nodeId=self.id).get('outerHTML')

    @outer_html.setter
    def outer_html(self, value):
        self.call('setOuterHTML', nodeId=self.id, outerHTML=value)

    def refresh_attributes(self):
        pairs = self.dom.call('getAttributes', nodeId=self.id).get('attributes', [])
        attrgen = (a for a in pairs)
        attrs = {}

        for name, value in [(n, attrgen.next()) for n in attrgen]:
            attrs[name] = value

        self.attributes = attrs

        return self.attributes

    @property
    def children(self):
        out = []

        for i in self.child_ids:
            el = self.dom.element(i)

            if el:
                out.append(el)

        return out

    def recheck_box(self):
        self._box_model = None
        return self.box

    def recheck_bounds(self):
        self._bounding_rect = None
        return self.bounds

    @property
    def bounds(self):
        if self._bounding_rect is None:
            self._bounding_rect = self.evaluate("return this.getBoundingClientRect()")
        return self._bounding_rect

    @property
    def box(self):
        if self._box_model is None:
            self._box_model = self.dom.call('getBoxModel', nodeId=self.id).get('model')

        return self._box_model

    @property
    def parent(self):
        return self.dom.element(self.parent_id)

    @property
    def width(self):
        return int(math.ceil(self.bounds.get('width', self.box['width'])))

    @property
    def height(self):
        return int(math.ceil(self.bounds.get('height', self.box['height'])))

    @property
    def top(self):
        return self.bounds.get('top')

    @property
    def right(self):
        return self.bounds.get('right')

    @property
    def bottom(self):
        return self.bounds.get('bottom')

    @property
    def left(self):
        return self.bounds.get('left')

    def query(self, selector):
        return self.dom.query(selector, node_id=self.id)

    def query_all(self, selector):
        return self.dom.query_all(selector, node_id=self.id)

    def xpath(self, expression):
        """
        Query the DOM for elements matching the given XPath expression, starting
        from the current element.

        #### Arguments

        - **expression** (`str`):

            An XPath expression to evaluate within the current DOM.

        #### Returns
        A list of matching elements.
        """
        return self.dom.xpath(expression, node_id=self.id)

    def remove(self):
        self.dom.remove(self.id)

    def focus(self):
        self.dom.focus(self.id)

    def __getitem__(self, key):
        return self.attributes[key]

    def __contains__(self, key):
        return (key in self.attributes)

    def __setitem__(self, key, value):
        self.dom.call('setAttributeValue', nodeId=self.id, name=key, value=str(value))

    def __delitem__(self, key):
        self.dom.call('removeAttribute', nodeId=self.id, name=key)

    def __repr__(self):
        if self.name:
            if self.type == 1:
                element_name = self.name.lower()
                attrs = []

                for k, v in self.attributes.items():
                    attrs.append('{}="{}"'.format(k, v))

                if len(attrs):
                    attrs = ' ' + ' '.join(attrs)
                else:
                    attrs = ''

                return '<{}{}>{}</{}>'.format(
                    element_name,
                    attrs,
                    self.text,
                    element_name
                )
            else:
                return '{} id={}'.format(self.name, self.id)
        else:
            parts = ['node={}'.format(self.id)]

            if self.name:
                parts.append('name={}'.format(self.name))

            return 'DOMElement<{}>'.format(','.join(parts))

    def __str__(self):
        return self.__repr__()


class DOM(Base):
    domain = 'DOM'
    _you_never_forget_your_first_root_element = None
    _root_element = None
    _elements = {}

    def initialize(self):
        self.on('setChildNodes', self.on_child_nodes)
        self.on('childNodeInserted', self.on_child_inserted)
        self.on('childNodeRemoved', self.on_child_removed)
        self.tab.page.on('frameClearedScheduledNavigation', self.reset)

    def reset(self, *args, **kwargs):
        """
        Clears out any existing local definitions in the DOM tree. This is used when navigating
        between pages so that the new remote DOM can be stored.
        """
        self._root_element = None

        if kwargs.get('clear_initial_root', True):
            self._you_never_forget_your_first_root_element = None

    def clear_requests(self, *args, **kwargs):
        self.tab.reset_network_request_cache()

    def has_element(self, id):
        """
        Return whether we know about the given element ID or not.

        #### Arguments

        - **id** (`str`):

            The DOM element id.
        """
        if id in self._elements:
            return True
        return False

    def element(self, id, fallback=None):
        """
        Return the given ID as a `webfriend.rpc.dom.DOMElement`, or `None` if we have not
        received the element from Chrome.

        #### Arguments

        - **id** (`str`):

            The DOM element id.

        - **fallback** (any):

            The value to return if the element is not known.

        #### Returns
        - `webfriend.rpc.dom.DOMElement` if the element is known, **fallback** if not.
        """
        return self._elements.get(id, fallback)

    def element_at(self, x, y, shadow=False):
        """
        Return the topmost `webfriend.rpc.dom.DOMElement` at the given page coordinates, or `None`
        if there is no element there.

        #### Arguments

        - **x** (`int`):

            The X-coordinate to test at.

        - **y** (`int`):

            The Y-coordinate to test at.

        - **shadow** (`bool`):

            If specified, include "shadow DOMs" in the query; see
            https://developers.google.com/web/fundamentals/getting-started/primers/shadowdom

        #### Returns
        - `webfriend.rpc.dom.DOMElement` if an element is at the coordinates, `None` if not.
        """
        node_id = self.call(
            'getNodeForLocation',
            x=x,
            y=y,
            includeUserAgentShadowDOM=shadow
        ).get('nodeId')

        if node_id:
            return self.element(node_id)

        return None

    def print_node(self, node_id=None, level=0, indent=4):
        """
        Print details about the given element to the debug log.
        """
        if node_id is None:
            node_id = self.root.id

        node = self.element(node_id)

        if node is not None:
            logging.debug('TREE: {}{}'.format((' ' * indent * level), node))

            for child in node.children:
                self.print_node(child.id, level=level + 1)

    @property
    def root(self):
        """
        Returns the root DOM element for the current document.

        #### Returns
        The `webfriend.rpc.dom.DOMElement` representing the root element.
        """
        if self._root_element is None:
            self.reset()

            self._root_element = DOMElement(
                self,
                self.call('getDocument', depth=1, pierce=True).get('root')
            )

            # keep track of the VERY first root element encountered, so that if we switch roots
            # for traversing frames, we can always come back to this one
            if self._you_never_forget_your_first_root_element is None:
                self._you_never_forget_your_first_root_element = self._root_element

            self._elements[self._root_element.id] = self._root_element

        return self._root_element

    @property
    def scroll_width(self):
        return self.root.evaluate(
            "return document.documentElement.scrollWidth",
            return_by_value=True
        ).get('value', None)

    @property
    def scroll_height(self):
        return self.root.evaluate(
            "return document.documentElement.scrollHeight",
            return_by_value=True
        ).get('value', None)

    @property
    def frames(self):
        return self.query_all('frame')

    def root_to(self, selector):
        elements = self.select_nodes(selector, wait_for_match=True)

        if elements:
            element = self.ensure_unique_element(selector, elements['nodes'])

            subdoc = element.content_document

            if subdoc is not None:
                # reset, we've got a document, but leave the top-level document in place
                # so we can go back to it
                self.reset(clear_initial_root=False)

                self.call('requestChildNodes', nodeId=subdoc.id)
                self._root_element = subdoc
                logging.debug('DOM root is now {}'.format(self.root))
                return self.root
            else:
                raise InvalidElement("Element does not contain a nested document")

        raise NoSuchElement("No elements matched the query selector '{}'".format(selector))

    def root_to_top(self):
        if self._you_never_forget_your_first_root_element:
            self._root_element = self._you_never_forget_your_first_root_element

        logging.debug('DOM root is now {}'.format(self.root))
        return self.root

    def remove_node(self, node_id):
        """
        Remove a specific node (and all children) from the DOM.

        - **id** (`str`):

            The DOM element id.
        """
        self.call('removeNode', nodeId=node_id)

    def focus(self, node_id):
        """
        Set the focus on a specific element.

        - **id** (`str`):

            The DOM element id.
        """
        self.call('focus', nodeId=node_id)

    def query(self, selector, node_id=None, reply_timeout=None):
        """
        Query for a single element.  Matched elements will be populated in the local DOM element
        cache for rapid retrieval in subsequent calls.

        - **selector** (`str`):

            The page element to query for, given as a CSS-style selector, an ID (e.g. "#myid"), or
            an XPath query (e.g.: "xpath://body/p").

        - **node_id** (`str`):

            If specified, the query will be performed relative to the element with the given
            Node ID.  Otherwise, the root element will be used.

        - **reply_timeout** (`int`):

            The timeout (in milliseconds) before the query raises a
            `webfriend.exceptions.TimeoutError`.

        #### Returns
        The matching `webfriend.rpc.dom.DOMElement`.

        #### Raises
        - `webfriend.exceptions.EmptyResult` if zero elements were matched, or
        - `webfriend.exceptions.TooManyResults` if more than one elements were matched.
        - `webfriend.exceptions.TimeoutError` if the query times out.
        """
        if node_id is None:
            node_id = self.root.id

        # perform the call
        matched_node_id = self.call(
            'querySelector',
            reply_timeout=reply_timeout,
            selector=self.prepare_selector(selector),
            nodeId=node_id
        ).get('nodeId')

        if not matched_node_id:
            raise NoSuchElement(
                "No elements matched the query selector '{}' under document {}".format(
                    selector,
                    node_id
                )
            )

        # we try to retrieve the element from the local element cache because they typically
        # come in as a series of events before the querySelector reply comes back, meaning that
        # by the time we get to this point we _should_ have cached definitions
        #
        # if we don't have a cached copy, then return a skeleton instance so that we can still
        # perform operations on the returned element
        #
        return self.element(matched_node_id, DOMElement(self, {
            'nodeId': matched_node_id,
        }))

    def query_all(self, selector, node_id=None, reply_timeout=None):
        """
        Query for all matching elements. Matched elements will be populated in the local DOM element
        cache for rapid retrieval in subsequent calls.

        - **selector** (`str`):

            The page element to query for, given as a CSS-style selector, an ID (e.g. "#myid"), or
            an XPath query (e.g.: "xpath://body/p").

        - **node_id** (`str`):

            If specified, the query will be performed relative to the element with the given
            Node ID.  Otherwise, the root element will be used.

        - **reply_timeout** (`int`):

            The timeout (in milliseconds) before the query raises a
            `webfriend.exceptions.TimeoutError`.

        #### Returns
        A `list` of matching `webfriend.rpc.dom.DOMElement` (zero or more).

        #### Raises
        - `webfriend.exceptions.TimeoutError` if the query times out.
        """
        if node_id is None:
            node_id = self.root.id

        # perform the call
        node_ids = self.call(
            'querySelectorAll',
            reply_timeout=reply_timeout,
            selector=self.prepare_selector(selector),
            nodeId=node_id
        ).get('nodeIds', [])

        # we try to retrieve the element from the local element cache because they typically
        # come in as a series of events before the querySelector reply comes back, meaning that
        # by the time we get to this point we _should_ have cached definitions
        #
        # if we don't have a cached copy, then return a skeleton instance so that we can still
        # perform operations on the returned element
        #
        return [
            self.element(i, DOMElement(self, {
                'nodeId': i,
            })) for i in node_ids
        ]

    def xpath(self, expression, wait_for_match=True, timeout=10000, interval=250):
        """
        Query the DOM for elements matching the given XPath expression.

        #### Arguments

        - **expression** (`str`):

            An XPath expression to evaluate within the current DOM.

        #### Returns
        A list of matching elements.
        """

        # call getDocument first so subsequent calls to performSearch work properly
        # (thanks @jamcplusplus for catching this)
        self.root
        started_at = time.time()

        while time.time() < (started_at + (timeout / 1000.0)):
            try:
                # perform the call
                handle = self.perform_search(expression)
                count = handle.get('resultCount', 0)

                if count:
                    return self.get_search_results(handle.get('searchId'), to_index=count)
                else:
                    self.discard_search_results(handle.get('searchId'))

            except (
                exceptions.TimeoutError,
                exceptions.ProtocolError
            ):
                pass

            if not wait_for_match:
                break

            time.sleep(interval / 1000.0)

        return False

    def select_nodes(self, selector, wait_for_match=True, timeout=10000, interval=250):
        """
        Polls the DOM for an element that matches the given selector.  Either the element will be
        found and returned within the given timeout, or a TimeoutError will be raised.

        #### Arguments

        - **selector** (`str`):

            The CSS-style selector that specifies the DOM element to look for.

        - **timeout** (`int`):

            The number of milliseconds to wait for the element to be returned.

        - **interval** (`int`):

            The polling interval, in milliseconds, used for rechecking for the element.

        #### Returns
        `webfriend.rpc.dom.DOMElement`

        #### Raises
        `webfriend.exceptions.TimeoutError`
        """
        started_at = time.time()

        while time.time() <= (started_at + (timeout / 1000.0)):
            try:
                elements = self.query_all(selector, reply_timeout=interval)

                # if we're not waiting or we are and we've got elements, return
                if not wait_for_match or len(elements):
                    results = {
                        'selector': selector,
                        'count':    len(elements),
                        'nodes': [
                            self.element(e.id, e) for e in elements
                        ],
                    }

                    if not len(results['nodes']):
                        return False

                    return results
            except (
                exceptions.TimeoutError,
                exceptions.ProtocolError
            ):
                pass

            time.sleep(interval / 1000.0)

        return False

    def on_child_nodes(self, event):
        for node in event.get('nodes', []):
            element = DOMElement(self, node)

            logging.debug('Adding node {} {}'.format(
                element.id,
                element
            ))

            self._elements[node['nodeId']] = element

            if self.has_element(element.parent_id):
                self.element(element.parent_id).child_ids.add(element.id)

    def on_child_inserted(self, event):
        definition = event.get('node')
        parent_id = event.get('parentNodeId')

        element = DOMElement(self, definition)
        self._elements[element.id] = element

        logging.debug('Inserting node {} {}'.format(
            element.id,
            element
        ))

        if self.has_element(parent_id):
            try:
                self.element(parent_id).child_ids.add(element.id)
            except KeyError:
                pass

    def on_child_removed(self, event):
        node_id = event.get('nodeId')
        parent_id = event.get('parentNodeId')

        if self.has_element(parent_id):
            try:
                self.element(parent_id).child_ids.remove(node_id)
            except KeyError:
                pass

        if self.has_element(node_id):
            logging.debug('Removing node {} {}'.format(
                self._elements[node_id].id,
                self._elements[node_id]
            ))

            del self._elements[node_id]

    # def on_set_attribute_value()

    @property
    def resources(self):
        return self.tab._network_requests

    def get_resource(self, url=None, request_id=None):
        """
        Return a `dict` describing a specific network resource, or false if none was found.

        #### Arguments

        - **url** (`str`, optional):

            If specified, this is the URL of the requested resource to retrieve.

        - **request_id** (`str`, optional):

            If specified, this is the specific resource to retrieve by Request ID.

        #### Returns
        A `dict` representing the resource, or _false_ if a match was not found.
        """
        if not request_id and not url:
            raise ValueError("Must specify either url or request_id")

        if request_id:
            return self.tab.get_network_request(request_id)
        elif url:
            matching_requests = []

            for _, request in self.resources.items():
                try:
                    if url == request['request']['url']:
                        return request
                    elif url in request['request']['url']:
                        matching_requests.append(request)
                except KeyError:
                    continue

            if len(matching_requests) == 1:
                return matching_requests[0]
            elif len(matching_requests) > 1:
                raise exceptions.TooManyResults(
                    'The URL pattern "{}" matched {} requests, need at most 1'.format(
                        url,
                        len(matching_requests)
                    )
                )

        return False

    @classmethod
    def prepare_selector(cls, selector):
        return selector

    @classmethod
    def ensure_unique_element(cls, selector, elements):
        if elements is False:
            raise exceptions.EmptyResult("No elements matched the selector: {}".format(
                selector
            ))

        if isinstance(elements, dict):
            nodes = elements.get('nodes', [])
        else:
            nodes = elements

        if not len(nodes):
            raise exceptions.EmptyResult("No elements matched the selector: {}".format(
                selector
            ))

        elif len(nodes) > 1:
            raise exceptions.TooManyResults(
                "Selector {} is ambiguous, matched {} elements".format(
                    selector, len(nodes)
                )
            )

        return nodes[0]

    def perform_search(self, query, shadow=True):
        params = {
            'query': query,
        }

        if shadow:
            params['includeUserAgentShadowDOM'] = shadow

        return self.call('performSearch', **params)

    def get_search_results(self, search_id, from_index=0, to_index=0):
        node_ids = self.call(
            'getSearchResults',
            searchId=search_id,
            fromIndex=from_index,
            toIndex=to_index
        ).get('nodeIds', [])

        return [
            self.element(i, DOMElement(self, {
                'nodeId': i,
            })) for i in node_ids
        ]

    def discard_search_results(self, search_id):
        self.call('discardSearchResults', searchId=search_id)

    def push_node_by_path_to_frontend(self, path):
        node_ids = self.call('pushNodeByPathToFrontend', path=path).get('nodeIds', [])

        return [
            self.element(i, DOMElement(self, {
                'nodeId': i,
            })) for i in node_ids
        ]

    def push_node_by_backend_ids_to_frontend(self, backend_node_ids):
        return self.call('pushNodesByBackendIdsToFrontend', backendNodeIds=backend_node_ids)

    def request_node(self, remote_object):
        return self.call('requestNode', objectId=remote_object).get('nodeId')
