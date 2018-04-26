from tests import CompilerTestCase
from wfc.errors import CompilationError


class TestIntent(CompilerTestCase):
    def test_intent_success(self):
        self._compile_to_json('intent')

    def test_intent_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json_with_failure('intent-bad-syntax')
