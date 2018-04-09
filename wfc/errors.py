class WFCError(Exception):
    def __init__(self, arg, *args):
        Exception.__init__(self, arg, *args)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, Exception.__str__(self))


class CarouselNotDefined(WFCError):
    pass


class CompilationError(WFCError):
    pass


class FlowNotDefined(WFCError):
    pass


class InvalidOutputFormat(WFCError):
    pass
