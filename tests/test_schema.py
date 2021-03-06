import unittest

from wfc.errors import SchemaViolationError
from wfc.schema import SchemaValidator
from tests.util import mixins


class TestSchemaValidator(unittest.TestCase, mixins.SampleHandler):
    def setUp(self):
        self.maxDiff = None
        self.validator = SchemaValidator()

    def _insert_action_ids(self, script):
        if 'dialogs' in script:
            for dialog in script['dialogs']:
                for action in dialog['actions']:
                    action['id'] = 'any'

        if 'flows' in script:
            for dialog in script['flows']:
                for action in dialog['actions']:
                    action['id'] = 'any'

    def test_validate_correct_v2_1_0_script(self):
        script = self.load_json_script('ask-210.json')
        self._insert_action_ids(script)
        self.assertTrue(self.validator.execute(script))

    def test_validate_incorrect_action_v2_1_0(self):
        script = self.load_json_script('ask-210.json')
        script['flows'][0]['actions'][0] = {
            'meh': {'text': 'Does not matter'}
        }
        self._insert_action_ids(script)
        with self.assertRaises(SchemaViolationError) as failure:
            self.validator.execute(script)

        expected_error = self.load_sample('ask-yaml.err').read()
        self.assertEquals(expected_error[:-1], str(failure.exception))
