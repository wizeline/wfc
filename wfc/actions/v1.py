from uuid import uuid4
from enum import Enum

from parglare.actions import pass_none

from wfc import Flow


class InputSource(Enum):
    INLINE = 0
    FILE = 1


def raw_value(_, value):
    return value


def read_examples(examples):
    return examples['value']


def string_value(_, value):
    return value[1:-1]


def operator_value(_, value):
    return value[0].replace(' ', '_')


def integer_value(_, value):
    return int(value)


def example_file_value(_, nodes):
    return {'source': InputSource.FILE, 'value': str(nodes[1])}


def example_list_value(_, nodes):
    values = nodes if nodes else None
    if values:
        return {'source': InputSource.INLINE, 'value': values[0]}


def definition_value(_, nodes):
    """
    DEFINE /intent|entity/ IDENTIFIER EXAMPLES
    """
    _, def_type, def_name, examples = nodes
    value = {
        'name': def_name,
        'examples': read_examples(examples)
    }
    if def_type == 'intent':
        Flow.INTENTIONS[def_name] = value
    elif def_type == 'entity':
        Flow.ENTITIES[def_name] = value

    return value


def action_value(_, nodes):
    action = nodes[0]
    action['id'] = str(uuid4())
    return action


def object_value(_, nodes):
    """
    IDENTIFIER MEMBER*
    """
    return nodes[0] + ''.join(nodes[1])


def prefixed_value(_, nodes):
    """
    PERIOD IDENTIFIER
    """
    return nodes[0] + nodes[1]


def bot_says_value(_, nodes):
    """
    say STRING
    """
    value = {
        'action': 'send_text',
        'text': ''.join(nodes[1])
    }
    return value


def reply_value(_, nodes):
    """
    reply STRING SET_ENTITY?
    """
    return nodes[1], nodes[2]


def quick_replies_value(_, nodes):
    """
    with COLON REPLIES
    """
    replies, fallback = nodes[2]

    entities = []
    expect = {}
    quick_replies = []

    for text, entity in replies:
        quick_replies.append(text)
        if entity is not None:
            entities.append(entity[1][1:])  # <'as' @entity> becomes <entity>

    if entities:
        expect['fallback'] = fallback
        expect['entities'] = entities

    return quick_replies, expect


def fallback_value(_, nodes):
    return nodes[1]


def bot_asks_value(_, nodes):
    """
    ask STRING+ as IDENTIFIER QUICK_REPLIES?
    """
    _, questions, _, var_name, replies = nodes
    value = {
        'text': ''.join(questions),
        'action': 'ask_for_input',
        'var_name': var_name
    }

    if replies:
        quick_replies, expect = replies

        value['quick_replies'] = quick_replies

        if expect:
            value['expect'] = expect
        else:
            # TODO: REVIEW THE RIGHT USE OF THIS
            value['can_switch_context'] = False

    return value


def bot_waits_value(_, nodes):
    """
    wait IDENTIFIER
    """
    return {'action': 'wait_input', 'var_name': nodes[1]}


def change_dialog_value(_, nodes):
    """
    change dialog IDENTIFIER DIALOG_PARAMETER?
    """
    _, _, dialog, _ = nodes

    value = {
        'action': 'change_dialog',
        'dialog': dialog
    }
    return value


def control_statement_value(_, nodes):
    """
    /if|when/ EXPRESSION COLON ACTION
    """
    _, expression, _, action = nodes
    action['condition'] = expression
    return action


def block_value(_, nodes):
    """
    STATEMENT | DO STATEMENT+ DONE
    """
    try:
        return nodes[1]
    except IndexError:
        return nodes[0]


def dialog_value(_, nodes):
    """
    dialog IDENTIFIER DIALOG_INTENT? BLOCK
    """

    _, name, dialog_intent, block = nodes
    value = {
        'name': name,
        'actions': block
    }

    if dialog_intent is not None:
        intent = dialog_intent[1][1:]
        if intent in Flow.INTENTIONS:
            Flow.INTENTIONS[intent]['dialog'] = name

    Flow.DIALOGS[name] = value
    return value


def call_function_value(_, nodes):
    """
    CALL_FUNCTION: 'call' IDENTIFIER PERIOD IDENTIFIER PARAMETERS?;
    """
    _, integration, _, fname, params = nodes

    params = [] if params is None else params[1]

    value = {
        'action': 'call_integration',
        'integration': integration,
        'function': fname,
        'function_params': params
    }

    return value


def attribute_value(_, nodes):
    """
    IDENTIFIER IDENTIFIER
    """
    return nodes[1], nodes[2]


def define_carousel_value(_, nodes):
    """
    CAROUSEL: 'carousel' IDENTIFIER COLON ATTRIBUTES;
    """
    _, name, _, attributes = nodes

    content = {}
    for attribute, value in attributes:
        content[attribute] = '{{' + '${}'.format(value) + '}}'

    Flow.CAROUSELS[name] = content


def send_carousel_value(_, nodes):
    """
    SEND_CAROUSEL: 'show' IDENTIFIER 'using' EXPRESSION
                   'and' 'pick' IDENTIFIER;
    """
    _, name, _, source, _, _, variable = nodes

    value = {
        'action': 'send_carousel',
        'content_source': source,
        'card_content': Flow.CAROUSELS[name]
    }

    return value


def build_actions():
    return {
        'ACTION': action_value,
        'ATTRIBUTE': attribute_value,
        'BLOCK': block_value,
        'BOT_ASKS': bot_asks_value,
        'BOT_SAYS': bot_says_value,
        'BOT_WAITS': bot_waits_value,
        'CAROUSEL': define_carousel_value,
        'CALL_FUNCTION': call_function_value,
        'CHANGE_DIALOG': change_dialog_value,
        'COMMENT': pass_none,
        'DEFINITION': definition_value,
        'DIALOG': dialog_value,
        'ENTITY': prefixed_value,
        'EXAMPLE_FILE': example_file_value,
        'EXAMPLE_LIST': example_list_value,
        'FALLBACK': fallback_value,
        'IF': control_statement_value,
        'INTEGER': integer_value,
        'INTENT': prefixed_value,
        'MEMBER': prefixed_value,
        'OBJECT': object_value,
        'OPERATOR': operator_value,
        'REPLY': reply_value,
        'QUICK_REPLIES': quick_replies_value,
        'SEND_CAROUSEL': send_carousel_value,
        'STRING': string_value,
        'VARIABLE': prefixed_value,
    }
