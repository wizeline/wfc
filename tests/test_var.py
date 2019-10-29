from tests import CompilerTestCase


class TestVar(CompilerTestCase):
    def test_var_success(self):
        self._compile('var')

    def test_var_with_bad_syntax(self):
        self._compile_with_failure('var-bad-syntax')

    def test_array_var(self):
        self._compile('set-array-var')

    def test_object_var(self):
        self._compile('set-object-var')

    def test_arithmetic_var(self):
        self._compile('arithmetic')

    def test_member_var(self):
        self._compile('set-member-var')

    def test_json_var(self):
        self._compile('set-json-var')
