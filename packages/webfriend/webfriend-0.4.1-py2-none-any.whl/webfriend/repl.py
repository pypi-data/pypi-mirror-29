from __future__ import absolute_import
from __future__ import unicode_literals
import json
import logging
import re
from webfriend.scripting.environment import Environment
from webfriend.scripting.scope import Scope
from webfriend.scripting.execute import execute_script
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments
from prompt_toolkit.token import Token
from webfriend.scripting.parser.pygments import FriendscriptLexer
from pygments.styles.monokai import MonokaiStyle


class FriendscriptCompleter(Completer):
    def __init__(self, commands, *args, **kwargs):
        self.commands = commands
        super(FriendscriptCompleter, self).__init__(*args, **kwargs)

    def get_completions(self, document, complete_event):
        line = document.current_line.lstrip()

        for command in self.commands:
            if command.startswith(line):
                yield Completion(command, start_position=len(line) - len(command))


class REPL(object):
    INTERNAL_COMMANDS = [
        'help',
    ]

    prompt = '(friendscript) '

    def __init__(self, browser, environment=None):
        self.browser = browser

        if environment:
            self.environment = environment
        else:
            self.environment = Environment(Scope(), browser=self.browser)

        self.completer = FriendscriptCompleter(
            sorted(self.environment.get_command_names())
        )
        self.history = InMemoryHistory()
        self.last_result = None
        self.echo_results = True

    def get_last_result(self, cli):
        toolbar = []

        if isinstance(self.last_result, Exception):
            toolbar.append((Token.Error, str(self.last_result)))

        return toolbar

    def run(self):
        while True:
            line = prompt(
                '{}'.format(self.prompt),
                lexer=PygmentsLexer(FriendscriptLexer),
                style=style_from_pygments(MonokaiStyle, {
                    Token.Error: '#ansiwhite bg:#ansired',
                }),
                completer=self.completer,
                history=self.history,
                get_bottom_toolbar_tokens=self.get_last_result
            )

            try:
                self.last_result = execute_script(
                    self.browser,
                    line,
                    environment=self.environment,
                    preserve_state=True
                )

                self.environment.set_scope(self.last_result)

                if self.echo_results and not self.is_internal_command(line):
                    print(json.dumps(self.last_result.as_dict(), indent=4))

            except Exception as e:
                self.last_result = e
                logging.exception('FAIL')
                print(e)

    def is_internal_command(self, line):
        parts = re.split(r'\s+', line)

        if len(parts) and parts[0] in self.INTERNAL_COMMANDS:
            return True

        return False
