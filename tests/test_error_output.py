import os
import sys
import unittest

from wfc import cli
from tests import SAMPLES_HOME
from tests.util import mixins


class TestErrorOutput(unittest.TestCase, mixins.SampleHandler):
    def setUp(self):
        self.output = '/tmp/errores.txt'

    def try_to_compile(self, *flows):
        stderr = sys.stderr
        with open(self.output, 'w') as output:
            sys.stderr = output
            sys.argv = [
                'wfc',
                '-w', SAMPLES_HOME,
                ' '.join(flows)
            ]
            cli.main()
        sys.stderr = stderr

    def load_output(self):
        with open(self.output) as output:
            return output.read()

    def load_expected_output(self, file_name):
        with open(os.path.join(SAMPLES_HOME, file_name)) as output:
            return output.read()

    def run_test(self, error_file, *modules):
        self.try_to_compile(*modules)
        with self.load_sample(error_file) as expected_error:
            self.assertEquals(
                expected_error.read(),
                self.load_output()
            )

    def test_ask_bad_syntax(self):
        self.run_test('ask-bad-syntax.err',
                      'ask-bad-syntax.flow')
