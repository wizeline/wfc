import json
import os
import sys
import unittest

from wfc import core
from wfc.cli import make_argument_parser

from tests.util import mixins


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
SAMPLES_HOME = os.path.join(TESTS_HOME, 'samples')


class CompilerTestCase(unittest.TestCase,
                       mixins.SampleHandler,
                       mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self._sys_stderr = sys.stderr
        self.arg_parser = make_argument_parser()
        self.maxDiff = None

        sys.stderr = self.open_tmpout()

    def tearDown(self):
        sys.stderr = self._sys_stderr
        self.unlink_tmpio()

    def _compile(self, test_target):
        self._compile_version(test_target, '2.1.0')
        self._compile_version(test_target, '2.2.0')

    def _compile_version(self, test_target, version):
        version_suffix = version.replace('.', '')
        script = self._compile_sample(test_target, version)
        self._prune_action_ids(script)

        expected_script = self.load_json_script(
            f'{test_target}-{version_suffix}.json'
        )
        self.assertDictEqual(expected_script, script)

    def _compile_with_failure(self, test_target):
        with self.assertRaises(AssertionError):
            self._compile_sample(test_target, '2.1.0')

    def _compile_sample(self, sample_name, out_version):
        compiled_script_path = self.get_tmp_path()
        rc = self._compile_with_args([
            '-o', compiled_script_path,
            '-w', SAMPLES_HOME,
            '-v', out_version,
            f'{sample_name}.flow'
        ])

        with self.open_tmpin() as compiled_sample:
            assert rc == 0, (f'Compilation failed with status {rc}\n'
                             f'Compiler output: {compiled_sample.read()}')

            if out_version in ('2.1.0', '2.2.0'):
                return json.load(compiled_sample)

    def _compile_with_args(self, args):
        with core.CompilerContext(self.arg_parser.parse_args(args)) as context:
            context.set_quiet()
            return core.compile(context)

    def _prune_action_ids(self, script):
        if 'flows' in script:
            for dialog in script['flows']:
                for action in dialog['actions']:
                    action.pop('id')
