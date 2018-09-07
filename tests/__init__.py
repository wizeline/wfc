import json
import os
import sys
import unittest

import yaml

from wfc import core
from wfc.cli import make_argument_parser
from wfc.commons import OutputVersion

from unittest.mock import MagicMock
from tests.util import mixins


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
SAMPLES_HOME = os.path.join(TESTS_HOME, 'samples')


class CompilerTestCase(unittest.TestCase, mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self._sys_stderr = sys.stderr
        self.arg_parser = make_argument_parser()
        self.maxDiff = None

        sys.stderr = self.open_tmpout()

    def tearDown(self):
        sys.stderr = self._sys_stderr
        self.unlink_tmpio()

    def _mock_output(self, context, tstin, tstout):
        context.get_input_file = MagicMock(name='get_input_file')
        context.get_output_file = MagicMock(name='get_output_file')
        context.get_input_file.return_value = tstin
        context.get_output_file.return_value = tstout

    def _compile(self, test_target):
        script = self._compile_sample(test_target, '2.0.0')
        self._prune_action_ids(script)

        expected_script = self._load_json_script(f'{test_target}.json')
        self.assertDictEqual(expected_script, script)

        script = self._compile_sample(test_target, '2.1.0')
        expected_script = self._load_yaml_script(f'{test_target}.yaml')
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

    def _load_json_script(self, script_name):
        with self._load_sample(script_name) as script_file:
            return json.load(script_file)

    def _load_sample(self, sample_name):
        sample_path = os.path.join(SAMPLES_HOME, sample_name)
        return open(sample_path, 'r')

    def _load_yaml_script(self, script_name):
        with self._load_sample(script_name) as script_file:
            return yaml.load(script_file)

    def _prune_action_ids(self, script):
        for dialog in script['dialogs']:
            for action in dialog['actions']:
                action.pop('id')
