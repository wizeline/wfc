class WFCError(Exception):
    def __init__(self, arg, *args):
        Exception.__init__(self, arg, *args)

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                               Exception.__str__(self))


class CompilationError(WFCError):
    pass


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
