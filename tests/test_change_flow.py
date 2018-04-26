from wfc import errors

from tests import CompilerTestCase


class TestChangeFlow(CompilerTestCase):
    def test_change_flow_success(self):
        self._compile_to_json('change-flow')

    def test_change_unexisting_flow(self):
        with self.assertRaises(errors.UndefinedFlow):
            self._compile_to_json_with_failure('change-unexisting-flow')

    def test_change_flow_with_bad_syntax(self):
        with self.assertRaises(errors.ParseError):
            self._compile_to_json_with_failure('change-flow-bad-syntax')
