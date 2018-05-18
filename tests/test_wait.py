from tests import CompilerTestCase


class TestWait(CompilerTestCase):
    def test_wait_success(self):
        self._compile_to_json('wait')
