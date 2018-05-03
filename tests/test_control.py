from wfc import errors

from tests import CompilerTestCase


class TestControl(CompilerTestCase):
    def test_control_success(self):
        self._compile_to_json('control')

    def test_control_with_bad_syntax(self):
        with self.assertRaises(errors.ParseError):
            self._compile_to_json('control-with-bad-syntax')

    def test_has_entity(self):
        self._compile_to_json('has-entity')
