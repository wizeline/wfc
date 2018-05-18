from tests import CompilerTestCase


class TestControl(CompilerTestCase):
    def test_control_success(self):
        self._compile_to_json('control')

    def test_control_with_bad_syntax(self):
        self._compile_to_json_with_failure('control-with-bad-syntax')

    def test_has_entity(self):
        self._compile_to_json('has-entity')

    def test_is_not_empty(self):
        self._compile_to_json('if-condition-is-not-empty')

    def test_is_not_condition_bad_syntax(self):
        self._compile_to_json_with_failure('if-condition-is-not-other')
