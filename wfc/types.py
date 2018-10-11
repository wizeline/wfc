from enum import Enum


class __WFCEnum(Enum):
    @classmethod
    def is_valid(cls, value):
        return any(value == member.value for service in cls)


class ComponentType(__WFCEnum):
    BUTTON = 'button'
    CAROUSEL = 'carousel'
    COMMAND = 'command'
    ENTITY = 'entity'
    FLOW = 'flow'
    INTEGRATION = 'integration'
    INTENT = 'intent'
    MENU = 'menu'


class FlowType(__WFCEnum):
    VOID = None
    FALLBACK = 'fallback'
    QNA = 'qna'


class InputSource(__WFCEnum):
    INLINE = 0
    FILE = 1
