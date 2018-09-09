from tests import CompilerTestCase


class TestFallbackFlow(CompilerTestCase):
    def test_fallback_flow_success(self):
        self._compile('fallback-flow')

    def test_fallback_flow_redefinition(self):
        self._compile_with_failure('fallback-flow-redefinition')

    def test_fallback_with_bad_syntax(self):
        self._compile_with_failure('fallback-flow-bad-syntax')
