import json

from uuid import uuid4
from enum import Enum

import jsonschema

from jsonschema.exceptions import ValidationError
from parglare.actions import pass_none

from wfc.commons import asset_path
from wfc.errors import (
    CompilationError,
    ComponentNotDefined,
    DynamicCarouselMissingSource,
    StaticCarouselWithSource,
    UndefinedCarousel
)

_script = None


class InputSource(Enum):
    INLINE = 0
    FILE = 1


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


def equals_value(_, nodes):
    """
    EQUALS: OBJECT 'equals' EXPRESSION;
    """
    return nodes


def definition_value(context, nodes):
    """
    DEFINE /intent|entity/ IDENTIFIER EXAMPLES
    """
    _, def_type, def_name, examples = nodes
    value = {
        'name': def_name,
        'examples': read_examples(examples)
    }
    _script.add_component(context, def_type, def_name, value)
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


def parameters_value(_, nodes):
    return [str(p) for p in nodes[1]]


def prefixed_value(_, nodes):
    """
    PERIOD IDENTIFIER
    """
    return nodes[0] + nodes[1]


def is_not_empty_value(_, nodes):
    """
    IS_NOT_EMPTY: VARIABLE is not? empty
    """
    variable, _, negative, _ = nodes
    if negative is None:
        return [variable, 'is_empty']
    else:
        return [variable, 'is_not_empty']


def has_entity_value(_, nodes):
    """
    HAS_ENTITY: OBJECT 'has' 'entity' ENTITY';
    """
    obj, _, _, entity = nodes
    return [obj, 'has_entity', entity[1:]]


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


def change_flow_value(context, nodes):
    """
    change flow IDENTIFIER FLOW_PARAMETER?
    """
    _, _, flow, _ = nodes

    if not _script.has_component('flow', flow):
        _script.ask_missing_component('flow', flow, context)

    return {
        'action': 'change_dialog',  # Right now the action is change_dialog
        'dialog': flow
    }


def control_statement_value(_, nodes):
    """
    /if|when/ EXPRESSION COLON ACTION
    """
    _, expression, _, action = nodes
    action['condition'] = expression
    return action


def if_statement_value(_, nodes):
    """
    if CONDITION COLON ACTION
    """
    _, condition, _, action, else_action = nodes

    action['condition'] = condition

    if else_action is not None:
        else_action['condition'] = not_condition(condition)
        actions = [action, else_action]

    else:
        actions = [action]

    return actions


def not_condition(condition):
    negatives = {
        'is_empty': 'is_not_empty',
        'has_entity': 'has_not_entity'
    }
    not_condition = list(condition)
    not_condition[1] = negatives[condition[1]]
    return not_condition


def else_value(_, nodes):
    return nodes[2]


def block_value(_, nodes):
    """
    STATEMENT | DO STATEMENT+ DONE
    """
    statements = []
    try:
        for statement in nodes[1]:
            if isinstance(statement, dict):
                statements.append(statement)
            elif isinstance(statement, list):
                statements.extend(statement)
    except IndexError:
        statements = nodes[0]

    return statements


def flow_value(context, nodes):
    """
    flow IDENTIFIER FLOW_INTENT? BLOCK
    """

    _, name, flow_intention, block = nodes
    value = {
        'name': name,
        'actions': block
    }

    if flow_intention is not None:
        intent = flow_intention[1][1:]
        try:
            intent_component = _script.get_component(context, 'intent', intent)
            intent_component['dialog'] = name
        except ComponentNotDefined:
            pass

    _script.add_component(context, 'flow', name, value)
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
    ATTRIBUTE: 'set' IDENTIFIER IDENTIFIER
    """
    return nodes[1], nodes[2]


def card_body_value(_, nodes):
    """
    CARD_BODY: ATTRIBUTE+[SEPARATOR] BUTTON_DEFINITION*[SEPARATOR];
    """
    attributes, buttons = nodes[0], nodes[1]

    card_body = {name: value for name, value in attributes}
    if buttons:
        card_body['buttons'] = buttons

    return card_body


def card_value(_, nodes):
    """
    CARD: 'card' COLON CARD_BODY;
    """
    return nodes[2]


def carousel_body_value(_, nodes):
    """
    CAROUSEL_BODY: CARD_BODY | CARDS+
    """
    if isinstance(nodes[0], list):
        return {'cards': nodes[0]}
    else:
        return {'card_content': nodes[0]}


def define_carousel_value(context, nodes):
    """
    CAROUSEL: 'carousel' IDENTIFIER COLON CAROUSEL_BODY 'end';
    """
    _, identifier, _, carousel_body, _ = nodes
    _script.add_component(context, 'carousel', identifier, carousel_body)


def carousel_content_source_value(_, nodes):
    """
    CAROUSEL_CONTENT_SOURCE: 'using' EXPRESSION;
    """
    return nodes[1]


def send_carousel_value(context, nodes):
    """
    SEND_CAROUSEL: 'show' IDENTIFIER ['using' EXPRESSION];
    """
    _, name, source = nodes
    try:
        carousel = _script.get_component(context, 'carousel', name)
    except ComponentNotDefined as ex:
        raise UndefinedCarousel(context, name)

    send_carousel = {'action': 'send_carousel'}
    send_carousel.update(carousel)

    if 'card_content' in carousel:
        if not source:
            raise DynamicCarouselMissingSource(context, name)

        send_carousel.update({'content_source': source})

    elif source:
        raise StaticCarouselWithSource(context, name)

    return send_carousel


def url_button_value(_, nodes):
    """
    URL_BUTTON: 'url' OPEN STRING SEPARATOR STRING CLOSE;
    """
    label, url = nodes[2], nodes[4]

    return {
        'label': label,
        'payload': url,
        'type': 'open_url'
    }


def postback_attribute_value(_, nodes):
    """
    POSTBACK_ATTRIBUTE: IDENTIFIER COLON STRING;
    """
    return nodes[0], nodes[2]


def postback_button_value(_, nodes):
    """
    POSTBACK_BUTTON: 'postback' OPEN
        STRING SEPARATOR POSTBACK_ATTRIBUTE+[SEPARATOR]
    CLOSE;
    """
    label, attributes = nodes[2], nodes[4]
    payload = {}
    for key, name in attributes:
        payload.update({key: name})

    return {
        'label': label,
        'payload': payload,
        'type': 'postback'
    }


def button_value(_, nodes):
    return nodes[0]


def button_definition_value(_, nodes):
    """
    BUTTON_DEFINITION: 'button' BUTTON;
    """
    return nodes[1]


def build_actions() -> dict:
    return {
        'ACTION': action_value,
        'ATTRIBUTE': attribute_value,
        'BLOCK': block_value,
        'BOT_ASKS': bot_asks_value,
        'BOT_SAYS': bot_says_value,
        'BOT_WAITS': bot_waits_value,
        'BUTTON': button_value,
        'BUTTON_DEFINITION': button_definition_value,
        'CALL_FUNCTION': call_function_value,
        'CARD': card_value,
        'CARD_BODY': card_body_value,
        'CAROUSEL': define_carousel_value,
        'CAROUSEL_BODY': carousel_body_value,
        'CAROUSEL_CONTENT_SOURCE': carousel_content_source_value,
        'CHANGE_FLOW': change_flow_value,
        'COMMENT': pass_none,
        'DEFINITION': definition_value,
        'ELSE': else_value,
        'ENTITY': prefixed_value,
        'EXAMPLE_FILE': example_file_value,
        'EXAMPLE_LIST': example_list_value,
        'EQUALS': equals_value,
        'FALLBACK': fallback_value,
        'FLOW': flow_value,
        'IF': if_statement_value,
        'INTEGER': integer_value,
        'INTENT': prefixed_value,
        'IS_NOT_EMPTY': is_not_empty_value,
        'HAS_ENTITY': has_entity_value,
        'MEMBER': prefixed_value,
        'OBJECT': object_value,
        'OPERATOR': operator_value,
        'PARAMETERS': parameters_value,
        'POSTBACK_ATTRIBUTE': postback_attribute_value,
        'POSTBACK_BUTTON': postback_button_value,
        'QUICK_REPLIES': quick_replies_value,
        'REPLY': reply_value,
        'SEND_CAROUSEL': send_carousel_value,
        'STRING': string_value,
        'URL_BUTTON': url_button_value,
        'VARIABLE': prefixed_value,
    }


def build_intentions() -> list:
    intents = []
    for intent in _script.get_components_by_type('intent').values():
        if 'dialog' not in intent:
            raise CompilationError(
                None,
                'Intent not used: {}'.format(intent['name'])
            )
        intents.append(intent)
    return intents


def build_flows() -> list:
    try:
        flows = _script.get_components_by_type('flow')
        onboarding = flows.pop('onboarding')
        flows = [onboarding] + list(flows.values())
    except KeyError:
        flows = list(flows.values())

    return flows


def load_output_schema() -> dict:
    with open(asset_path('schema.json')) as schema:
        return json.loads(schema.read())


def get_script():
    _script.perform_sanity_checks()
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
        with open('/tmp/invalid.json', 'w') as invalid_script:
            invalid_script.write(json.dumps(script, indent=2))

        raise ValueError('Generated script does not match with schema',
                         script)


def set_script(script):
    global _script
    _script = script
