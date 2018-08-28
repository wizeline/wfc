import re

import parglare


class ErrorContext:
    """Extracts meaningful information from parglare context"""
    def __init__(self, context=None):
        if context:
            position = parglare.pos_to_line_col(context.input_str,
                                                context.start_position)
            self.line, self.column = position
        else:
            self.line, self.column = None, None


class WFCError(Exception):
    def __init__(self, parse_context, *args):
        super().__init__(*args)
        self.context = ErrorContext(parse_context)


class ComponentNotDefined(WFCError):
    pass


class ComponentNotSupprted(WFCError):
    pass


class ComponentRedefinition(WFCError):
    pass


class FlowNotDefined(WFCError):
    pass


class InvalidOutputFormat(WFCError):
    pass


class ParseError(WFCError):
    def __init__(self, context):
        self.context = context

    def __str__(self):
        message = self._extract_error_message()
        return '{}:Syntax error. {}'.format(self.context.line, message)

    def _extract_error_message(self):
        raw_message = self.context.args[0]
        message_pattern = r'Error at position .* => (.*) Expected.*'
        match = re.search(message_pattern, raw_message)
        return match.groups()[0]


class CompilationError(Exception):
    __format__ = '{}:{}'
    __message__ = '{}'

    def __init__(self, context, arg):
        self.message = self.__message__.format(arg)

        if context is None:
            self.context = None
            super().__init__(self.message)
        else:
            if isinstance(context, ErrorContext):
                self.context = context
            else:
                self.context = ErrorContext(context)

            super().__init__(self.__format__.format(self.context.line,
                                                    self.message))


class DynamicCarouselMissingSource(CompilationError):
    __message__ = 'Missing content source for dynamic carousel "{}"'


class StaticCarouselWithSource(CompilationError):
    __message__ = 'Static carousel "{}" must not have content source'


class UndefinedCarousel(CompilationError):
    __message__ = 'Carousel "{}" is not defined'


class UndefinedFlow(CompilationError):
    __message__ = 'Flow "{}" is not defined'
