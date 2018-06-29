from tests import CompilerTestCase


class TestChangeFlow(CompilerTestCase):
    def test_change_flow_success(self):
        self._compile_to_json('open-flow')

    def test_change_unexisting_flow(self):
        self._compile_to_json_with_failure('open-unexisting-flow')

    def test_change_flow_with_bad_syntax(self):
        self._compile_to_json_with_failure('open-flow-bad-syntax')
