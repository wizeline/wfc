from tests import CompilerTestCase


class TestIntent(CompilerTestCase):
    def test_intent_success(self):
        self._compile('intent')

    def test_intent_with_bad_syntax(self):
        self._compile_with_failure('intent-bad-syntax')
