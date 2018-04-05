import json
import os
import unittest

from tests import load_sample
from tests.util import mixins
from wfc.core import compile_source
from wfc.parser import create_parser


class TestCore(unittest.TestCase, mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.parser = create_parser()

    def _prune_action_ids(self, script):
        for dialog in script['dialogs']:
            for action in dialog['actions']:
                action.pop('id')

    def test_compile_source_success(self):
        expected_script = {
            "version": "1.0.0",
            "intentions": [],
            "entities": [],
            "dialogs": [
                {
                    "name": "say_hi",
                    "actions": [
                        {
                            "action": "send_text",
                            "text": "hi",
                        }
                    ]
                }
            ],
            "qa": []
        }

        with load_sample('hello.flow') as sample_flow:
            tmp_out = self.open_tmpout()
            compile_source(self.parser, os.curdir, sample_flow, tmp_out)
            tmp_out.close()

        with self.open_tmpin() as compiled_sample:
            script = json.load(compiled_sample)

        self._prune_action_ids(script)
        self.assertDictEqual(expected_script, script)
        self.unlink_tmpio()
