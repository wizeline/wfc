import json

from uuid import uuid4
from enum import Enum

import jsonschema

from jsonschema.exceptions import ValidationError
from parglare.actions import pass_none

from wfc.commons import asset_path
from wfc.errors import FlowNotDefined, CarouselNotDefined

_script = None


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
        _script.INTENTIONS[def_name] = value
    elif def_type == 'entity':
        _script.ENTITIES[def_name] = value

    return value


def action_value(_, nodes):
    action = nodes[0]
    try:
        action['id'] = str(uuid4())
    except TypeError as ex:
        print(ex, action, '<---- here')
        raise ex
    return action


def object_value(_, nodes):
    """
    IDENTIFIER MEMBER*
    """
    return nodes[0] + ''.join(nodes[1])


def parameters_value(_, nodes):
    return [str(p) for p in nodes[1]]

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


def change_flow_value(_, nodes):
    """
    change flow IDENTIFIER DIALOG_PARAMETER?
    """
    _, _, flow, _ = nodes

    if flow not in _script.FLOWS:
        raise FlowNotDefined(flow)

    value = {
        'action': 'change_dialog', # Right now the instruction is change_dialog
        'dialog': flow
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


def flow_value(_, nodes):
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
        if intent in _script.INTENTIONS:
            _script.INTENTIONS[intent]['dialog'] = name

    _script.FLOWS[name] = value
    return value


def call_function_value(_, nodes):
    """
    CALL_FUNCTION: 'call' IDENTIFIER PERIOD IDENTIFIER PARAMETERS?;
    """
    _, integration, _, fname, params = nodes

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
    CAROUSEL: 'carousel' IDENTIFIER COLON ATTRIBUTES 'end';
    """
    _, name, _, attributes, _ = nodes

    content = {}
    for attribute, value in attributes:
        content[attribute] = '{{' + '${}'.format(value) + '}}'

    _script.CAROUSELS[name] = content


def send_carousel_value(_, nodes):
    """
    SEND_CAROUSEL: 'show' IDENTIFIER 'using' EXPRESSION
                   'and' 'pick' IDENTIFIER;
    """
    _, name, _, source, _, _, variable = nodes

    try:
        value = {
            'action': 'send_carousel',
            'content_source': source,
            'card_content': _script.CAROUSELS[name]
        }
    except KeyError:
        raise CarouselNotDefined(name)

    return value


def build_actions(script: object) -> dict:
    global _script
    _script = script

    return {
        'ACTION': action_value,
        'ATTRIBUTE': attribute_value,
        'BLOCK': block_value,
        'BOT_ASKS': bot_asks_value,
        'BOT_SAYS': bot_says_value,
        'BOT_WAITS': bot_waits_value,
        'CAROUSEL': define_carousel_value,
        'CALL_FUNCTION': call_function_value,
        'CHANGE_FLOW': change_flow_value,
        'COMMENT': pass_none,
        'DEFINITION': definition_value,
        'FLOW': flow_value,
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
        'PARAMETERS': parameters_value,
        'REPLY': reply_value,
        'QUICK_REPLIES': quick_replies_value,
        'SEND_CAROUSEL': send_carousel_value,
        'STRING': string_value,
        'VARIABLE': prefixed_value,
    }


def build_intentions() -> list:
    intents = []
    for intent in _script.INTENTIONS.values():
        if 'dialog' not in intent:
            raise Exception('Intent not used: {}'.format(intent['name']))
        intents.append(intent)
    return intents


def build_flows() -> list:
    try:
        onboarding = _script.FLOWS.pop('onboarding')
        flows = [onboarding] + list(_script.FLOWS.values())
    except KeyError:
        flows = list(_script.FLOWS.values())

    return flows


def load_output_schema() -> dict:
    with open(asset_path('schema.json')) as schema:
        return json.loads(schema.read())


def get_script():
    try:
        script = {
            'version': "1.0.0",
            'intentions': build_intentions(),
            'entities': [],
            'dialogs': build_flows(),
            'qa': []
        }

        jsonschema.validate(script, load_output_schema())
        return json.dumps(script, indent=2)
    except ValidationError as ex:
        print(ex)
        raise ValueError('Generated script does not match with schema')
