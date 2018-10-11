import os
import re

import parglare


class ErrorContext:
    """Extracts meaningful information from parglare context"""
    def __init__(self, input_path='', context=None):
        self.input_path = os.path.basename(input_path)
        if context:
            position = parglare.pos_to_line_col(context.input_str,
                                                context.start_position)
            self.line, self.column = position
        else:
            self.line, self.column = None, None

    def has_input_path(self):
        return len(self.input_path) > 0

    def set_intpu_path(self, input_path):
        self.input_path = input_path


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
    def __init__(self, context, input_path='', *args):
        super().__init__(*args)

        if isinstance(context, ErrorContext):
            self.context = context
        else:
            self.context = ErrorContext(context=context)

        self.input_path = input_path or context.input_path

    def __str__(self):
        message = self._build_error_message()
        input_path = os.path.basename(self.input_path)
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
        return f'Intent not used: {self.args[0]}'


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
