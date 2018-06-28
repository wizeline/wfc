from tests import CompilerTestCase


class TestVar(CompilerTestCase):
    def test_var_success(self):
        self._compile_to_json('var')

    def test_var_with_bad_syntax(self):
        self._compile_to_json_with_failure('var-bad-syntax')
