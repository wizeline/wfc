from tests import CompilerTestCase


class TestConditional(CompilerTestCase):
    def test_conditional_with_else_clause_success(self):
        self._compile_to_json('if-then-else-success')
