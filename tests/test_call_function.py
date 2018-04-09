from tests import CompilerTestCase
from wfc.errors import CompilationError


class TestCallFunction(CompilerTestCase):
    def test_call_function_success(self):
        self._compile_to_json('call-function')

    def test_call_function_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json_with_failure('call-function-bad-syntax')
