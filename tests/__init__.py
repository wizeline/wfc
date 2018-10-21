import json
import os
import sys
import unittest

import yaml

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
        script = self._compile_sample(test_target, '2.0.0')
        self._prune_action_ids(script)

        expected_script = self.load_json_script(f'{test_target}.json')
        self.assertDictEqual(expected_script, script)

        script = self._compile_sample(test_target, '2.1.0')
        self._prune_action_ids(script)

        expected_script = self.load_yaml_script(f'{test_target}.yaml')
        self.assertDictEqual(expected_script, script)

    def _compile_with_failure(self, test_target):
        with self.assertRaises(AssertionError):
            self._compile_sample(test_target, '2.0.0')

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

            if out_version == '2.0.0':
                return json.load(compiled_sample)
            elif out_version == '2.1.0':
                return yaml.load(compiled_sample)

    def _compile_with_args(self, args):
        with core.CompilerContext(self.arg_parser.parse_args(args)) as context:
            context.set_quiet()
            return core.compile(context)

    def _prune_action_ids(self, script):
        if 'dialogs' in script:
            for dialog in script['dialogs']:
                for action in dialog['actions']:
                    action.pop('id')

        if 'flows' in script:
            for dialog in script['flows']:
                for action in dialog['actions']:
                    action.pop('id')
