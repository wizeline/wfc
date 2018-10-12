from tests import CompilerTestCase


class TestMenu(CompilerTestCase):
    def test_send_undefined_menu(self):
        self._compile_with_failure('send-undefined-menu')

    def test_send_carousel_with_bad_syntax(self):
        self._compile_with_failure('send-menu-with-bad-syntax')

    def test_send_menu_success(self):
        self._compile('menu')
