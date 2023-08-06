from __future__ import absolute_import
from __future__ import unicode_literals
import logging
import time
import io
from webfriend.scripting.commands.base import CommandProxy
from webfriend import exceptions


class PageProxy(CommandProxy):
    def screenshot(
        self,
        destination=None,
        width=0,
        height=0,
        x=-1,
        y=-1,
        format='png',
        jpeg_quality=None,
        selector=[],
        settle=250,
        after_events=None,
        settle_timeout=None,
        reply_timeout=30000,
        autoclose=True,
        use="tallest",
    ):
        """
        Capture the current screen contents as an image and write the image to a file or return it
        as a file-like object.

        #### Arguments

        - **destination** (`str`, _file-like object_, optional):

            If given as a string, this will be the filesystem path that the image is written to.
            If given as a file-like object, that object will be written to, seeked back to zero,
            and returned.  If `None`, an `io.BytesIO` buffer will be allocated, written to, and
            returned.

        - **width**, **height** (`int`, optional):

            If given, this is the width and/or height the viewport will be resized to before
            capturing the image. If not specified, the dimensions of the element specified by
            'selector' will be queried and that element's outerWidth/outerHeight will be used.

        - **x**, **y** (`int`, optional):

            If given, this is the x/y position the viewport will be moved to.  If a negative number
            is specified, then the x/y coordinates of the element matched by **selector** will be
            used.

        - **format** (`str`):

            The output format of the image, either `png` or `jpeg`.

        - **jpeg_quality** (`int`, optional):

            If given, and if **format** is `jpeg`, this is the quality of the JPEG image (0-100).

        - **selector** (`str`, `list`):

            When detecting the width and/or height of the page area to render, this is the HTML
            element that will be measured.  Changing this to a selector that matches a specific
            element (using the default settings for **width**, **height**, **x**, and **y**) will
            result in taking a screenshot of _just_ that element.

            If a `list` is specified, all elements in the list will be retrieved and the one with
            the largest height will be used.

        - **settle** (`int`, optional):

            The number of milliseconds to wait after performing the viewport resize before
            actually capturing the image.  This gives newly-exposed elements time to load.

        - **after_events** (`str`, `list`, optional):

            If an event name or list of event names is given, then **settle** will be interpreted
            as an amount of time _after_ the last of these named events has been received. If the
            special value `any` is provided, then **settle** will wait for that amount of time
            since any event has been received to elapse, up to 'settle_timeout' seconds.

        - **settle_timeout** (`int`, optional):

            The maximum amount of time to wait for events to stop coming in as described in by
            **after_events**.

        - **reply_timeout** (`int`, optional):

            The maximum amount of time to wait for the screenshot call to complete.

        - **autoclose** (`bool`):

            If a file handle is given as the **destination**, should it be automatically closed
            when the screenshot is completed.

        - **use** (`str`):

            Determines how to handle multiple elements that are matched by **selector**.

            - "tallest":
                Use the tallest element as the result for measuring screenshot dimensions.

            - "first":
                Use the first element matched as the result for measuring screenshot dimensions.

        #### Returns
        `dict`, with keys:

        - _element_ (`webfriend.rpc.DOMElement`):
            The element that was used as a measurement reference.

        - _width_ (`int`):
            The final width of the viewport that was captured.

        - _height_ (`int`):
            The final height of the viewport that was captured.

        - _x_ (`int`):
            The final X-position of the viewport that was captured.

        - _y_ (`int`):
            The final Y-position of the viewport that was captured.

        - _destination_ (`object`, optional):
            The destination file-like object data was written to, if specified.

        - _path_ (`str`, optional):
            The filesystem path of the file data was written to, if specified.
        """

        element = None
        stored_element = None
        is_explicitly_set = set()

        # width defaults to document scrollWidth
        if not width:
            width = self.tab.dom.scroll_width
        else:
            is_explicitly_set.add('width')

        # height defaults to document scrollHeight
        if not height:
            height = self.tab.dom.scroll_height
        else:
            is_explicitly_set.add('height')

        # listify selector
        if selector is None:
            selector = []
        elif not isinstance(selector, list):
            selector = [selector]

        # if selector is a list, then find the tallest element among all of them
        for s in selector:
            try:
                elements = self.tab.dom.query_all(s)
                element = self.tab.dom.ensure_unique_element(s, elements)

                if use == "tallest":
                    if stored_element:
                        if element.height > stored_element.height:
                            stored_element = element

                elif use == "first":
                    stored_element = element
                    break

                else:
                    raise exceptions.WebfriendError(
                        "Unrecognized use '{}'".format(use)
                    )

            except (exceptions.EmptyResult, exceptions.TooManyResults) as e:
                logging.debug("Screenshot selector error: {}".format(e))
                continue

        if stored_element:
            element = stored_element

        return_flo = True

        # ---
        # if an element was found and an explicit override was not set...
        if element:
            if 'width' not in is_explicitly_set:
                width = element.width

            if 'height' not in is_explicitly_set:
                height = element.height

            if x < 0:
                x = element.left
            else:
                x = 0

            if y < 0:
                y = element.top
            else:
                y = 0
        # ---

        capture_screenshot_params = {
            'format': format,
            'reply_timeout': reply_timeout,
        }

        # setup a FLO to write data to if we don't have one
        if destination is None:
            destination = io.BytesIO()
        elif isinstance(destination, basestring):
            return_flo = False

        if x > 0 or y > 0:
            capture_screenshot_params['clip'] = {
                'width':  width,
                'height': height,
                'x':      int(x),
                'y':      int(y),
                'scale':  1.0,
            }
        else:
            if width and height:
                # resize and force redraw
                self.tab.emulation.set_device_metrics_override(
                    width=width,
                    height=height,
                    device_scale_factor=1.0
                )

            self.tab.emulation.set_visible_size(width, height)
            self.tab.page.capture_screenshot(destination, **capture_screenshot_params)

            # wait for a spell for the page to adjust to its new world
            if settle:
                if after_events is None:
                    logging.info('Waiting {}ms for resize to settle'.format(settle))
                    time.sleep(settle / 1e3)
                else:
                    wfi_params = {}

                    if settle_timeout:
                        wfi_params['timeout'] = settle_timeout

                    if after_events != 'any':
                        wfi_params['event_filter'] = after_events

                    try:
                        logging.info('Waiting {}ms after last events'.format(settle))
                        self.tab.wait_for_idle(settle, **wfi_params)
                    except exceptions.TimeoutError:
                        pass

        out = {
            'element': element,
            'width':   width,
            'height':  height,
            'x':       x,
            'y':       y,
        }

        if return_flo:
            destination.seek(0)
            out['destination'] = destination

            if autoclose:
                if hasattr(destination, 'close'):
                    close = getattr(destination, 'close')

                    if callable(close):
                        close()
        else:
            out['path'] = destination

        try:
            self.tab.emulation.clear_device_metrics_override()
        except:
            pass

        try:
            self.tab.emulation.reset_viewport()
        except:
            pass

        try:
            self.tab.emulation.reset_page_scale_factor()
        except:
            pass

        return out

    def start_capture(
        self,
        destination,
        duration=None,
        format='png',
        jpeg_quality=85,
        every_nth=None,
        filename_format=None
    ):
        self.tab.page.start_screencast(
            destination=destination,
            duration=duration,
            format=format,
            jpeg_quality=jpeg_quality,
            every_nth=every_nth,
            filename_format=filename_format,
            additional_values=self.scope.as_dict()
        )

    def wait_for_capture(self):
        self.tab.wait_for('Page.screencastVisibilityChanged')

    def stop_capture(self):
        self.tab.page.stop_screencast()

    def find(self, text, **kwargs):
        logging.info('text={}, kwargs={}'.format(text, kwargs))
        raise exceptions.NotImplemented("find()")

    def source(self, selector=None):
        """
        Retrieves the `outerHtml` of the matching page element.

        #### Arguments

        - **selector** (`str`):

            The page element to retrieve source for, given as a CSS-style selector, an ID
            (e.g. "#myid"), or an XPath query (e.g.: "xpath://body/p").

        #### Returns
        A `unicode` string representing the HTML contents of the matched element.

        #### Raises
        - `webfriend.exceptions.EmptyResult` if zero elements were matched, or
        - `webfriend.exceptions.TooManyResults` if more than one elements were matched.
        """
        if selector:
            elements = self.tab.dom.select_nodes(selector)
            self.tab.dom.ensure_unique_element(selector, elements)
            return elements['nodes'][0].outer_html
        else:
            return self.tab.dom.root.outer_html

    # def highlight(self, selector, **kwargs):
    #     elements = self.tab.dom.select_nodes(selector)
    #     self.tab.dom.ensure_unique_element(selector, elements)
    #     self.tab.overlay.highlight_node(node_id=elements['nodes'][0].id, **kwargs)

    def remove(self, selector):
        """
        Removes ALL elements that match the given selector from the page.

        #### Arguments

        - **selector** (`str`):

            The page elements to remove, given as a CSS-style selector, an ID
            (e.g. "#myid"), or an XPath query (e.g.: "xpath://body/p").

        #### Returns
        A `list` of `webfriend.rpc.DOMElement` instances that were matched and removed from the
        page.
        """
        removed = []

        for element in self.tab.dom.query_all(selector):
            self.tab.dom.remove(element.id)
            removed.append(element)

        return removed

    def dump_dom(self):
        """
        Print the portion of the DOM the local page cache is currently aware of to log output.
        This is primarily useful for debugging WebFriend.
        """
        self.tab.dom.print_node()

    def resources(self):
        """
        Return a list of objects describing every network request that has occurred since the last
        invocation of `[go](#go)`, since the resource cache was last cleared with
        `[page::clear_resources](#pageclear_resources)`, or since the current tab was loaded.

        #### Returns
        A `list` of `dict` containing details about the network requests that were performed.
        """
        return self.tab.dom.resources.values()

    def resource(self, **kwargs):
        """
        See: `webfriend.rpc.DOM.get_resource`
        """
        request = self.tab.dom.get_resource(**kwargs)

        if request and request.get('completed'):
            out = {
                'id': request.get('id'),
                'request': request,
                'data': None,
            }

            try:
                out['data'] = io.BytesIO()
                out['data'].write(self.tab.network.get_response_body(request['id']))
                out['data'].seek(0)
            except:
                pass

            return out
        else:
            return False

    def save_resource(self, destination, **kwargs):
        res = self.resource(**kwargs)

        if 'id' in res:
            with open(destination, 'w') as f:
                f.write(self.tab.network.get_response_body(res['id']))

            return destination
        else:
            return False

    def dialog_cancel(self):
        """
        Cancels an open modal dialog (presses 'Cancel').
        """
        self.tab.page.dialog(False)

    def dialog_ok(self):
        """
        Accepts an open modal dialog (presses 'OK' or 'Yes').
        """
        self.tab.page.dialog(True)

    def prompt_text(self, text, submit=True):
        """
        Enters the given text into an open prompt dialog and (optionally) submits it.

        #### Arguments

        - **text** (`str`):

            The text value to enter into the prompt dialog.

        - **submit** (`bool`, optional):

            Whether to automatically submit the dialog or not.
        """
        self.tab.page.dialog(submit, text=text)
