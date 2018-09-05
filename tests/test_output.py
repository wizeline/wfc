import unittest
from unittest.mock import MagicMock

from wfc.errors import (
    ComponentNotDefined,
    ComponentNotSupprted,
    ComponentRedefinition
)
from wfc.output import Script


class TestScript(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.component = {'any': 'object'}
        self.name = 'any-object'
        self.context = MagicMock()
        self.script = Script(self.context)
        self.context.get_input_path.return_value = '/tmp/file.flow'

    def test_script_add_component_success(self):
        components = {
            'button': {},
            'carousel': {},
            'entity': {},
            'flow': {'is_fallback': False},
            'integration': {},
            'intent': {}
        }

        for component_type, component in components.items():
            self.script.add_component(None,
                                      component_type,
                                      self.name,
                                      component)
            stored_component = self.script.get_component(None, component_type,
                                                         self.name)
            self.assertEqual(stored_component, component)

    def test_script_add_unsupported_component(self):
        with self.assertRaises(ComponentNotSupprted):
            self.script.add_component(None, 'blah', 'any_name', {})

    def test_script_redefine_component(self):
        self.script.add_component(None, 'button', 'my_button', {})
        with self.assertRaises(ComponentRedefinition):
            self.script.add_component(None, 'button', 'my_button', {})

    def test_script_get_unexisting_component(self):
        with self.assertRaises(ComponentNotDefined):
            self.script.get_component(None, 'button', 'button')

        self.script.add_component(
            None,
            'flow',
            'onboarding',
            {
                'is_fallback': True,
                'name': 'onboarding'
            }
        )
        with self.assertRaises(ComponentNotDefined):
            self.script.get_component(None, 'flow', 'not_a_flow')
