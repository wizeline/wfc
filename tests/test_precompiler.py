import sys

from wfc import cli

from tests import CompilerTestCase, SAMPLES_HOME

class TestPrecompiler(CompilerTestCase):
    def test_include_twice(self):
        out_path = self.get_tmp_path()
        sys.argv = ['wfc', '-o', out_path, '-q', '-w', SAMPLES_HOME,
                    'first-include.flow', 'second-include.flow']
        self.assertEqual(0, cli.main())

