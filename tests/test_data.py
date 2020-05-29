from tests import CompilerTestCase


class TestData(CompilerTestCase):
    def test_data_success(self):
        self._compile_version('data', '2.2.0')
