from tests import CompilerTestCase


class TestWait(CompilerTestCase):
    def test_wait_success(self):
        self._compile('wait')

    def test_wait_with_quick_replies(self):
        self._compile('wait-expecting-entities')

    def test_wait_without_context_switching(self):
        self._compile('wait-keeping-context')
