from tests import CompilerTestCase


class TestAsk(CompilerTestCase):
    def test_ask_success(self):
        self._compile_to_json('ask')

    def test_ask_with_bad_syntax(self):
        self._compile_to_json_with_failure('ask-bad-syntax')

    def test_ask_with_quick_replies(self):
        self._compile_to_json('ask-with-quick-replies')

    def test_ask_without_fallback(self):
        self._compile_to_json('ask-without-fallback')
