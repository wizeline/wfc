import json
import os
import unittest

from tests.util import mixins
from wfc import core


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
SAMPLES_HOME = os.path.join(TESTS_HOME, 'samples')


class CompilerTestCase(unittest.TestCase, mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None

    def tearDown(self):
        self.unlink_tmpio()

    def _compile_to_json(self, test_target):
        script = self._compile_sample('{}.flow'.format(test_target))
        self._prune_action_ids(script)

        expected_script = self._load_json_script('{}.json'.format(test_target))
        self.assertDictEqual(expected_script, script)

    def _compile_to_json_with_failure(self, test_target):
        self._compile_sample('{}.flow'.format(test_target))

    def _compile_sample(self, sample_name):
        with self._load_sample(sample_name) as sample_script:
            tmp_out = self.open_tmpout()
            core.compile(
                in_script=sample_script,
                out_script=tmp_out,
                quiet=True
            )
            tmp_out.close()

        with self.open_tmpin() as compiled_sample:
            return json.load(compiled_sample)

    def _load_json_script(self, script_name):
        with self._load_sample(script_name) as script_file:
            return json.load(script_file)

    def _load_sample(self, sample_name):
        sample_path = os.path.join(SAMPLES_HOME, sample_name)
        return open(sample_path, 'r')

    def _prune_action_ids(self, script):
        for dialog in script['dialogs']:
            for action in dialog['actions']:
                action.pop('id')
