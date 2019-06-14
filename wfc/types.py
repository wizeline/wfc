import json
from enum import Enum


class __WFCEnum(Enum):
    @classmethod
    def is_valid(cls, value):
        return any(value == member.value for member in cls)

    def __str__(self):
        return self.value


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


class OutputVersion(__WFCEnum):
    V20 = '2.0.0'
    V21 = '2.1.0'


class ComponentDefinitionContext:
    def __init__(self, path, line):
        self.path = path
        self.line = line


class ConstantValue(__WFCEnum):
    NULL = None
    TRUE = True
    FALSE = False
    EMPTY = {}

    def __str__(self):
        return json.dumps(self.value)
