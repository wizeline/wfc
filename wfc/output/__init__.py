import os

from wfc.errors import (
    ComponentNotDefined,
    ComponentNotSupprted,
    ComponentRedefinition,
    ErrorContext,
    FallbackFlowRedefinition,
    InvalidOutputFormat,
    QNAFlowRedefinition,
    UndefinedCarousel,
    UndefinedFlow
)
from wfc.commons import OutputVersion
from wfc.output import v20, v21
from wfc.types import ComponentType

_VERSIONS = {
    OutputVersion.V20: v20,
    OutputVersion.V21: v21
}


class OutputBuilder:
    def __init__(self, script, version):
        if version not in _VERSIONS:
            raise InvalidOutputFormat(version)

        self._output_module = _VERSIONS[version]
        self._output_module.set_script(script)
        self._actions = self._output_module.build_actions()

    def get_actions(self):
        return self._actions

    def get_script(self):
        return self._output_module.get_script()


class Script:
    def __init__(self, compiler_context):
        self._asked_components = []
        self._components = {}
        self._fallback_flow = ''
        self._qna_flow = ''
        self.compiler_context = compiler_context

    def _get_current_file(self):
        return os.path.basename(self.compiler_context.get_input_path())

    def _raise_missing_component_error(self, component_type, name, context):
        if component_type == ComponentType.CAROUSEL:
            raise UndefinedCarousel(context, name)

        if component_type == ComponentType.FLOW:
            raise UndefinedFlow(context, name)

    def ask_missing_component(self, component_type, name, context):
        self._asked_components.append((
            component_type,
            name,
            ErrorContext(self._get_current_file(), context)
        ))

    def add_component(self, context, component_type, name, component):
        if not isinstance(component_type, ComponentType):
            raise ComponentNotSupprted(
                context,
                self.compiler_context.get_input_path(),
                component_type
            )

        if component_type == ComponentType.FLOW:
            is_fallback = component.pop('is_fallback')
            if is_fallback:
                if self._fallback_flow == '':
                    self._fallback_flow = component['name']
                else:
                    raise FallbackFlowRedefinition(
                        context,
                        self.compiler_context.get_input_path(),
                        self._fallback_flow,
                        component['name']
                    )

            is_qna = component.pop('is_qna')
            if is_qna:
                if self._qna_flow == '':
                    self._qna_flow = component['name']
                else:
                    raise QNAFlowRedefinition(
                        context,
                        self.compiler_context.get_input_path(),
                        self._fallback_flow,
                        component['name']
                    )

        components = self._components.get(component_type, {})

        if name in components:
            raise ComponentRedefinition(context, component_type, name)

        components[name] = component
        self._components.update({component_type: components})

    def get_component(self, context, component_type, name):
        components = self.get_components_by_type(component_type)
        try:
            return components[name]
        except KeyError:
            raise ComponentNotDefined(
                context,
                self.compiler_context.get_input_path(),
                name
            )

    def get_components_by_type(self, component_type):
        return self._components.get(component_type, {})

    def get_fallback_flow(self):
        return self._fallback_flow

    def get_qna_flow(self):
        return self._qna_flow

    def has_component(self, component_type, name):
        if not isinstance(component_type, ComponentType):
            raise ComponentNotSupprted(
                self.compiler_context,
                self.compiler_context.get_input_path(),
                component_type
            )
        return name in self._components.get(component_type, {})

    def perform_sanity_checks(self):
        while self._asked_components:
            component_type, name, context = self._asked_components.pop()
            if not self.has_component(component_type, name):
                self._raise_missing_component_error(
                    component_type,
                    name,
                    context
                )
