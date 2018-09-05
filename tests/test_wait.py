from tests import CompilerTestCase


class TestWait(CompilerTestCase):
    def test_wait_success(self):
        self._compile('wait')
