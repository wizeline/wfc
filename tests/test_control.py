from tests import CompilerTestCase
from wfc.errors import CompilationError


class TestControl(CompilerTestCase):
    def test_control_success(self):
        self._compile_to_json('control')

    def test_control_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json('control-with-bad-syntax')
