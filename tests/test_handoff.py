from tests import CompilerTestCase


class TestHandoff(CompilerTestCase):
    def test_handoff_success(self):
        self._compile('handoff')
