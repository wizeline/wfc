from tests import CompilerTestCase
from wfc.errors import CompilationError, DialogNotDefined


class TestAsk(CompilerTestCase):
    def test_change_dialog_success(self):
        self._compile_to_json('change-dialog')

    def test_change_unexisting_dialog(self):
        with self.assertRaises(DialogNotDefined):
            self._compile_to_json_with_failure('change-unexisting-dialog')

    def test_change_dialog_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json_with_failure('change-dialog-bad-syntax')
