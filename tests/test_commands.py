
from tests import CompilerTestCase


class TestCommands(CompilerTestCase):
    def test_commands_success(self):
        self._compile_to_json('commands')

    def test_commands_with_bad_syntax(self):
        self._compile_to_json_with_failure('commands-bad-syntax')

    def test_commands_with_undefined_flow(self):
        self._compile_to_json_with_failure('commands-with-undefined-flow')

    def test_commands_without_fallback(self):
        self._compile_to_json_with_failure('commands-redefinition')
