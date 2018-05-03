from enum import Enum

from wfc.errors import (
    InvalidOutputFormat,
    ComponentNotDefined,
    ComponentNotSupprted,
    ComponentRedefinition,
    ErrorContext,
    UndefinedCarousel,
    UndefinedFlow
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
        self._asked_components = []

    def _raise_missing_component_error(self, component_type, name, context):
        if component_type == 'carousel':
            raise UndefinedCarousel(context, name)

        if component_type == 'flow':
            raise UndefinedFlow(context, name)

    def ask_missing_component(self, component_type, name, context):
        self._asked_components.append((component_type,
                                       name,
                                       ErrorContext(context)))

    def add_component(self, context, component_type, name, component):
        try:
            component_type = ComponentType(component_type).value
            components = self._components.get(component_type, {})

            if name in components:
                raise ComponentRedefinition(context, component_type, name)

            components[name] = component
            self._components.update({component_type: components})
        except ValueError:
            raise ComponentNotSupprted(context, component_type)

    def get_component(self, context, component_type, name):
        try:
            component_type = ComponentType(component_type).value
            return self._components[component_type][name]
        except KeyError:
            raise ComponentNotDefined(context, name)
        except ValueError:
            raise ComponentNotSupprted(context, component_type)

    def get_components_by_type(self, component_type):
        try:
            component_type = ComponentType(component_type).value
            return self._components[component_type]
        except KeyError:
            return {}
        except ValueError:
            raise ComponentNotSupprted(None, component_type)

    def has_component(self, component_type, name):
        try:
            component_type = ComponentType(component_type).value
            return name in self._components[component_type]
        except (KeyError, ValueError):
            return False

    def perform_sanity_checks(self):
        while self._asked_components:
            component_type, name, context = self._asked_components.pop()
            if not self.has_component(component_type, name):
                self._raise_missing_component_error(component_type,
                                                    name,
                                                    context)


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
