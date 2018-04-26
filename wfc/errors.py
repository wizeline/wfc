import parglare


class WFCError(Exception):
    def __init__(self, arg, *args):
        Exception.__init__(self, arg, *args)


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


class CompilationError(WFCError):
    def __init__(self, cause, context, *args):
        super().__init__(cause, *args)
        self.line, self.column = self._get_position(context)

    def __str__(self):
        return 'Error at position {},{} => {}'.format(
            self.line,
            self.column,
            super().__str__()
        )

    def _get_position(self, context):
        return parglare.pos_to_line_col(context.input_str,
                                        context.start_position)


class ParseError(WFCError):
    def __init__(self, parse_error):
        self.parse_error = parse_error

    def __str__(self):
        return str(self.parse_error)


class DynamicCarouselMissingSource(CompilationError):
    def __init__(self, name, context):
        msg = 'Missing content source for dynamic carousel "{}"'.format(name)
        super().__init__(msg, context)


class StaticCarouselWithSource(CompilationError):
    def __init__(self, name, context):
        msg = 'Static carousel "{}" must not have content source'.format(name)
        super().__init__(msg, context)


class UndefinedCarousel(CompilationError):
    def __init__(self, name, context):
        msg = 'Carousel "{}" is not defined'.format(name)
        super().__init__(msg, context)


class UndefinedFlow(CompilationError):
    def __init__(self, name, context):
        msg = 'Flow "{}" is not defined'.format(name)
        super().__init__(msg, context)
