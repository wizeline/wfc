from tests import CompilerTestCase
from wfc import errors


class TestCarousel(CompilerTestCase):
    def test_send_carousel_success(self):
        self._compile_to_json('send-carousel')

    def test_send_undefined_carousel(self):
        with self.assertRaises(errors.CarouselNotDefined):
            self._compile_to_json_with_failure('send-undefined-carousel')

    def test_send_carousel_with_bad_syntax(self):
        with self.assertRaises(errors.CompilationError):
            self._compile_to_json_with_failure('send-carousel-with-bad-syntax')
