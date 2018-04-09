from tests import CompilerTestCase


class TestSay(CompilerTestCase):
    def test_say_success(self):
        self._compile_to_json('say')
