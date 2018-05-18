from tests import CompilerTestCase


class TestCarouselCommon(CompilerTestCase):
    def test_send_undefined_carousel(self):
        self._compile_to_json_with_failure('send-undefined-carousel')

    def test_send_carousel_with_bad_syntax(self):
        self._compile_to_json_with_failure('send-carousel-with-bad-syntax')


class TestDynamicCarousel(CompilerTestCase):
    def test_send_carousel_success(self):
        self._compile_to_json('dynamic-carousel')

    def test_send_carousel_with_buttons_success(self):
        self._compile_to_json('dynamic-carousel-with-buttons')

    def test_send_carousel_without_source(self):
        self._compile_to_json_with_failure('dynamic-carousel-without-source')


class TestStaticCarousel(CompilerTestCase):
    def test_send_carousel_success(self):
        self._compile_to_json('static-carousel')

    def test_send_carousel_with_buttons_success(self):
        self._compile_to_json('static-carousel-with-buttons')

    def test_send_carousel_with_source(self):
        self._compile_to_json_with_failure('static-carousel-with-source')
