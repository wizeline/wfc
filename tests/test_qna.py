from tests import CompilerTestCase


class TestQNAFollowupFlow(CompilerTestCase):
    def test_qna_flow_success(self):
        self._compile('qna-flow')

    def test_qna_flow_redefinition(self):
        self._compile_with_failure('qna-flow-redefinition')

    def test_qna_with_bad_syntax(self):
        self._compile_with_failure('qna-flow-bad-syntax')
