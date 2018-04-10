from tests import CompilerTestCase
from wfc.errors import CompilationError, ComponentNotDefined


class TestChangeFlow(CompilerTestCase):
    def test_change_flow_success(self):
        self._compile_to_json('change-flow')

    def test_change_unexisting_flow(self):
        with self.assertRaises(ComponentNotDefined):
            self._compile_to_json_with_failure('change-unexisting-flow')

    def test_change_flow_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json_with_failure('change-flow-bad-syntax')
