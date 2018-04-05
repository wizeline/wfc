import json
import os
import unittest

from tests import load_json_script, load_sample
from tests.util import mixins
from wfc.core import compile_source
from wfc.parser import create_parser


class TestCore(unittest.TestCase, mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.parser = create_parser()
        self.maxDiff = None

    def tearDown(self):
        self.unlink_tmpio()

    def _compile_sample(self, sample_name):
        with load_sample(sample_name) as sample_flow:
            tmp_out = self.open_tmpout()
            compile_source(self.parser, os.curdir, sample_flow, tmp_out)
            tmp_out.close()

        with self.open_tmpin() as compiled_sample:
            return json.load(compiled_sample)

    def _prune_action_ids(self, script):
        for dialog in script['dialogs']:
            for action in dialog['actions']:
                action.pop('id')

    def _compile_to_json(self, test_target):
        script = self._compile_sample('{}.flow'.format(test_target))
        self._prune_action_ids(script)

        expected_script = load_json_script('{}.json'.format(test_target))
        self.assertDictEqual(expected_script, script)

    def test_entity_success(self):
        self._compile_to_json('entity')

    def test_say_success(self):
        self._compile_to_json('say')

    def test_ask_success(self):
        self._compile_to_json('ask')

    def test_wait_success(self):
        self._compile_to_json('wait')

    def test_change_dialog_success(self):
        self._compile_to_json('change-dialog')

    def test_call_function_success(self):
        self._compile_to_json('call-function')

    def test_send_carousel_success(self):
        self._compile_to_json('send-carousel')

    def test_control_success(self):
        self._compile_to_json('control')

    def _test_send_media_success(self):
        # self._compile_to_json('send-media')
        pass

    def _test_send_menu_success(self):
        # self._compile_to_json('send-menu')
        pass

    def _test_open_flow(self):
        # Action not implemented
        # self._compile_to_json('send-menu')
        pass
