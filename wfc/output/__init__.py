from enum import Enum

from wfc.errors import (
    InvalidOutputFormat,
    ComponentNotDefined,
    ComponentNotSupprted,
    ComponentRedefinition
)
from wfc.output import v1

_FORMATS = {
    'v1': v1
}


class ComponentType(Enum):
    BUTTON = 'button'
    CAROUSEL = 'carousel'
    ENTITY = 'entity'
    FLOW = 'flow'
    INTEGRATION = 'integration'
    INTENT = 'intent'


class Script:
    def __init__(self):
        self._components = {}

    def add_component(self, component_type, name, component):
        try:
            component_type = ComponentType(component_type).value
            components = self._components.get(component_type, {})

            if name in components:
                raise ComponentRedefinition(component_type, name)

            components[name] = component
            self._components.update({component_type: components})
        except ValueError:
            raise ComponentNotSupprted(component_type)

    def get_component(self, component_type, name):
        try:
            component_type = ComponentType(component_type).value
            return self._components[component_type][name]
        except KeyError:
            raise ComponentNotDefined(name)
        except ValueError:
            raise ComponentNotSupprted(component_type)

    def get_components_by_type(self, component_type):
        try:
            component_type = ComponentType(component_type).value
            return self._components[component_type]
        except KeyError:
            return {}
        except ValueError:
            raise ComponentNotSupprted(component_type)

    def has_component(self, component_type, name):
        try:
            component_type = ComponentType(component_type).value
            return name in self._components[component_type]
        except (KeyError, ValueError):
            return False


def get_script(selected_format):
    try:
        return _FORMATS[selected_format].get_script()
    except KeyError:
        raise InvalidOutputFormat(selected_format)


def build_actions(selected_format='v1'):
    try:
        return _FORMATS[selected_format].build_actions(Script())
    except KeyError:
        raise InvalidOutputFormat(selected_format)
