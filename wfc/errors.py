class WFCError(Exception):
    pass


class CarouselNotDefined(WFCError):
    pass


class CompilationError(WFCError):
    pass


class DialogNotDefined(WFCError):
    pass


class InvalidOutputFormat(WFCError):
    pass
