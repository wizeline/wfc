from tests import CompilerTestCase
from wfc.errors import CompilationError


class TestEntity(CompilerTestCase):
    def test_entity_success(self):
        self._compile_to_json('entity')

    def test_entity_with_bad_syntax(self):
        with self.assertRaises(CompilationError):
            self._compile_to_json_with_failure('entity-bad-syntax')
