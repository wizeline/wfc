import unittest

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
        self.script = Script()

    def test_script_add_component_success(self):
        for component_type in ('button', 'carousel', 'entity', 'flow',
                               'integration', 'intent'):
            self.script.add_component(component_type, self.name, self.name)
            component = self.script.get_component(component_type, self.name)
            self.assertEqual(self.name, component)

    def test_script_add_unsupported_component(self):
        with self.assertRaises(ComponentNotSupprted):
            self.script.add_component('blah', 'any_name', {})

    def test_script_redefine_component(self):
        self.script.add_component('button', 'my_button', {})
        with self.assertRaises(ComponentRedefinition):
            self.script.add_component('button', 'my_button', {})

    def test_script_get_unexisting_component(self):
        with self.assertRaises(ComponentNotDefined):
            self.script.get_component('button', 'button')

        self.script.add_component('flow', 'onboarding', {})
        with self.assertRaises(ComponentNotDefined):
            self.script.get_component('flow', 'not_a_flow')
