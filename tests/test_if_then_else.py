from tests import CompilerTestCase


class TestConditional(CompilerTestCase):
    def test_conditional_with_else_clause_success(self):
        self._compile('if-then-else-success')
