import json
import os
import re

import parglare

from wfc.types import OutputVersion


class ErrorContext:
    """Extracts meaningful information from parglare context"""
    def __init__(self, input_path, context):
        self.input_path = os.path.abspath(input_path)
        if context:
            position = parglare.pos_to_line_col(context.input_str,
                                                context.start_position)
            self.line, self.column = position
        else:
            self.line, self.column = None, None


class SchemaViolationError(Exception):
    def __init__(self, validation_error, script, version):
        self.error = validation_error
        self.script = script
        self.version = version

    def _get_action_index(self):
        return self.error.path[1]

    def _get_flow_name(self):
        if self.version == OutputVersion.V20:
            return self.script[self.error.path[0]][self.error.path[1]]['name']
        elif self.version == OutputVersion.V21:
            return self.script[self.error.path[0]][self.error.path[1]]['name']

    def __str__(self):
        flow_name = self._get_flow_name()
        action_index = self._get_action_index()
        failed_instance = json.dumps(self.error.instance, indent=2)
        return (f'Script does not meet schema for version {self.version} '
                f'at action {flow_name}[{action_index}]\n'
                f'{failed_instance}')


class InvalidOutputFormat(Exception):
    def __str__(self):
        return f'Invalid script version: {self.args[0]}'


class WFCError(Exception):
    def __init__(self, parse_context, *args):
        super().__init__(*args)
        self.context = ErrorContext(parse_context)


class ParseError(WFCError):
    def __init__(self, context, input_path):
        self.context = context
        self.input_path = os.path.basename(input_path)

    def __str__(self):
        message = self._extract_error_message()
        return f'{self.input_path}:{self.context.line}:Syntax error. {message}'

    def _extract_error_message(self):
        raw_message = self.context.args[0]
        message_pattern = r'Error at position .* => (.*) Expected.*'
        match = re.search(message_pattern, raw_message)
        return match.groups()[0]


class CompilationError(Exception):
    def __init__(self, context, *args):
        assert isinstance(context,
                          ErrorContext), f'Bad context {type(context)}'
        super().__init__(*args)
        self.context = context

    def __str__(self):
        message = self._build_error_message()
        input_path = os.path.basename(self.context.input_path)
        return f'{input_path}:{self.context.line}:{message}'

    def _build_error_message(self):
        return super().__str__()


class ComponentNotDefined(CompilationError):
    def _build_error_message(self):
        return f'Component {self.args[0]} is not defined'


class ComponentNotSupprted(CompilationError):
    def _build_error_message(self):
        return f'Component {self.args[0]} is not supported'


class FallbackFlowRedefinition(CompilationError):
    def _build_error_message(self):
        return ('Fallback flow must be unique: '
                f'[{self.args[0]}] [{self.args[1]}]')


class FlowNotDefined(CompilationError):
    def _build_error_message(self):
        return f'Flow {self.args[0]} is not defined'


class UnusedIntent(CompilationError):
    def _build_error_message(self):
        return f'Intent "{self.args[0]}" is not used'


class DynamicCarouselMissingSource(CompilationError):
    def _build_error_message(self):
        return f'Missing content source for dynamic carousel {self.args[0]}'


class StaticCarouselWithSource(CompilationError):
    def _build_error_message(self):
        return f'Static carousel "{self.args[0]}" must not have content source'


class QNAFlowRedefinition(CompilationError):
    def _build_error_message(self):
        return f'QNA flow must be uniq: [{self.args[0]}] [{self.args[1]}]'


class UndefinedCarousel(CompilationError):
    def _build_error_message(self):
        return f'Carousel "{self.args[0]}" is not defined'


class UndefinedComponent(CompilationError):
    def _build_error_message(self):
        return f'Component "{self.args[0]}" is not defined'


class UndefinedFlow(CompilationError):
    def _build_error_message(self):
        return f'Flow "{self.args[0]}" is not defined'


class ComponentRedefinition(CompilationError):
    def _build_error_message(self):
        return f'Redefinition of {self.args[0]} "{self.args[1]}"'


class CardTitleEmptyError(CompilationError):
    def _build_error_message(self):
        return f'Card title should not be empty'
