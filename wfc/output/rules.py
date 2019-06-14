from uuid import uuid4

from parglare.actions import pass_none

from wfc.errors import (
    CardTitleEmptyError,
    ComponentNotDefined,
    DynamicCarouselMissingSource,
    EmptyMenuMissingSource,
    ErrorContext,
    StaticCarouselWithSource,
    UndefinedComponent,
    WaitInputWithQuickReplies
)
from wfc.types import ComponentType, FlowType, InputSource, ConstantValue

_script = None


def read_examples(examples):
    return examples['value']


def string_value(_, value):
    return value[1:-1]


def get_expression_value(expression):
    if isinstance(expression, ConstantValue):
        return expression.value
    return expression


def subscribe_feed_value(_, nodes):
    return {
        'action': 'subscribe_feed',
        'feed': nodes[1]
    }


def unsubscribe_feed_value(_, nodes):
    return {
        'action': 'unsubscribe_feed',
        'feed': nodes[1]
    }


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
    EQUALS: VARIABLE 'not'? 'equal' EXPRESSION;
    """
    variable, negative, _, expression = nodes
    operator = 'equal' if negative is None else 'not_equal'
    return [variable, operator, get_expression_value(expression)]


def constant_value(context, nodes):
    value = nodes[0]
    if value == 'false':
        return ConstantValue.FALSE
    if value == 'true':
        return ConstantValue.TRUE
    if value == 'nil':
        return ConstantValue.NULL
    if value == 'empty':
        return ConstantValue.EMPTY
    return nodes


def definition_value(context, nodes):
    """
    DEFINE /intent|entity/ IDENTIFIER EXAMPLES
    """
    _, def_type_name, def_name, examples = nodes
    value = {
        'name': def_name,
        'examples': read_examples(examples)
    }
    def_type = ComponentType(def_type_name)

    _script.add_component(context, def_type, def_name, value)
    return value


def action_value(_, nodes):
    action = nodes[0]
    if isinstance(action, dict):
        action['id'] = str(uuid4())
    elif isinstance(action, list):
        for a in action:
            a['id'] = str(uuid4())

    return action


def object_value(_, nodes):
    """
    IDENTIFIER MEMBER*
    """
    return nodes[0] + ''.join(nodes[1])


def parameters_value(_, nodes):
    return list(map(get_expression_value, nodes[1]))


def prefixed_value(_, nodes):
    """
    PERIOD IDENTIFIER
    """
    return nodes[0] + nodes[1]


def member_definiiton_value(_, nodes):
    return nodes[0], nodes[2]


def define_menu_value(context, nodes):
    """
    MENU_BODY: COLON BUTTON_DEFINITION+[SEPARATOR] 'end';
    MENU: 'menu' IDENTIFIER STRING? MENU_BODY?;
    """
    _, name, text, body = nodes

    menu = {'buttons': body[1]} if body else {}
    if text:
        menu['text'] = text

    _script.add_component(context, ComponentType.MENU, name, menu)
    return nodes


def is_empty_value(_, nodes):
    """
    IS_EMPTY: VARIABLE is not? empty
    """
    variable, _, negative, _ = nodes
    if negative is None:
        return [variable, 'is_empty']
    else:
        return [variable, 'is_not_empty']


def literal_object_value(_, nodes):
    return {member: value for member, value in nodes[0]}


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
    reply REPLY_BODY
    """
    return nodes[1]


def reply_body_value(_, nodes):
    """
    STRING SET_ENTITY? | ENTITY
    """
    if len(nodes) == 1:
        return None, nodes[0]
    elif nodes[1] is not None:
        return nodes[0], nodes[1][1]
    else:
        return nodes[0], None


def quick_replies_value(_, nodes):
    """
    with COLON REPLIES
    """
    replies, fallback = nodes[2]

    entities = []
    expect = {}
    quick_replies = []

    for text, entity in replies:
        if text is not None:
            quick_replies.append(text)
        if entity is not None:
            entities.append(entity[1:])  # <@entity> becomes <entity>

    if entities:
        expect['fallback'] = fallback
        expect['entities'] = entities

    return quick_replies, expect


def fallback_value(_, nodes):
    return nodes[1]


def bot_asks_value(_, nodes):
    """
    ask STRING+ as IDENTIFIER KEEP_CONTEXT? QUICK_REPLIES?
    """
    _, questions, _, var_name, context_switch, replies = nodes
    value = {
        'text': ''.join(questions),
        'action': 'ask_for_input',
        'var_name': var_name
    }

    if replies:
        quick_replies, expect = replies

        if quick_replies:
            value['quick_replies'] = quick_replies

        if expect:
            value['expect'] = expect

    if context_switch:
        value['can_switch_context'] = False

    return value


def bot_waits_value(context, nodes):
    """
    wait IDENTIFIER KEEP_CONTEXT? QUICK_REPLIES?
    """
    # wait_input action does not support quick replies but it supports
    # expecting entities. So we admit quick replies from the grammar but only
    # keep the expect and context switching features.
    _, variable, context_switch, replies = nodes

    value = {
        'action': 'wait_input',
        'var_name': variable
    }

    if replies:
        quick_replies, expect = replies

        if quick_replies:
            raise WaitInputWithQuickReplies(ErrorContext(
                _script.get_current_file(),
                context
            ))

        if expect:
            value['expect'] = expect

    if context_switch:
        value['can_switch_context'] = False

    return value


def change_flow_value(context, nodes):
    """
    change flow IDENTIFIER FLOW_PARAMETER?
    """
    _, _, flow, _ = nodes

    if not _script.has_component(ComponentType.FLOW, flow):
        _script.ask_missing_component(ComponentType.FLOW, flow, context)

    return {
        'action': 'change_dialog',  # Right now the action is change_dialog
        'dialog': flow
    }


def define_command_value(context, nodes):
    """
    when read STRING do IDENTIFIER
    """
    _, _, keyword, _, flow = nodes

    if not _script.has_component(ComponentType.FLOW, flow):
        _script.ask_missing_component(ComponentType.FLOW, flow, context)

    command = {
        'keyword': keyword,
        'dialog': flow
    }

    _script.add_component(
        context,
        ComponentType.COMMAND,
        keyword,
        command
    )


def open_flow_value(context, nodes):
    """
    open flow IDENTIFIER
    """
    _, _, flow = nodes

    if not _script.has_component(ComponentType.FLOW, flow):
        _script.ask_missing_component(ComponentType.FLOW, flow, context)

    return {
        'action': 'open_flow',  # Right now the action is change_dialog
        'flow': flow
    }


def control_statement_value(_, nodes):
    """
    /if|when/ EXPRESSION COLON ACTION
    """
    _, expression, _, action = nodes
    action['condition'] = expression
    return action


def if_statement_value(context, nodes):
    """
    if CONDITION IF_BODY
    """
    _, condition, if_body = nodes
    actions, else_actions = if_body
    for action in actions:
        action['condition'] = condition

    if else_actions not in (None, 'end'):
        negative = not_condition(condition)
        for else_action in else_actions:
            else_action['condition'] = negative
        actions += else_actions

    return actions


def if_body_value(_, nodes):
    """
    IF_BODY: COLON ACTION ELSE? | ACTION+ IF_CLOSURE
    """
    if nodes[0] == ':':
        actions = [nodes[1]]
        else_actions = nodes[2]
    else:
        actions = nodes[0]
        else_actions = nodes[1]

    return [actions, else_actions]


def if_closure_value(_, nodes):
    """
    IF_CLOSURE: 'end' | ELSE
    """
    if nodes[0] == 'end':
        return None
    else:
        return nodes[0]


def not_condition(condition):
    negatives = {
        'is_empty': 'is_not_empty',
        'has_entity': 'has_not_entity',
        'equal': 'not_equal'
    }

    not_condition = list(condition)
    not_condition[1] = negatives[condition[1]]
    return not_condition


def else_body_value(_, nodes):
    """
    ELSE_BODY: COLON ACTION | ACTION+ END;
    """

    if nodes[0] == ':':
        return [nodes[1]]
    else:
        return nodes[0]


def else_value(_, nodes):
    return nodes[1]


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
    FLOW_TYPE? flow IDENTIFIER FLOW_INTENT? BLOCK
    """

    flow_type_name, _, name, flow_intention, block = nodes
    value = {
        'name': name,
        'actions': block
    }

    flow_type = FlowType(flow_type_name)

    if flow_intention is not None:
        intent = flow_intention[1][1:]
        try:
            intent_component, _ = _script.get_component(
                context,
                ComponentType.INTENT,
                intent
            )
            intent_component['dialog'] = name
        except ComponentNotDefined:
            pass

    value['is_fallback'] = True if flow_type == FlowType.FALLBACK else False
    value['is_qna'] = True if flow_type == FlowType.QNA else False

    _script.add_component(
        context,
        ComponentType.FLOW,
        name,
        value
    )

    return value


def flow_type_value(context, nodes):
    """
    'fallback' | 'qna'
    """

    return nodes[0]


def call_function_value(context, nodes):
    """
    CALL_FUNCTION: 'call' IDENTIFIER PERIOD IDENTIFIER PARAMETERS? AS_VAR;
    """
    _, integration, _, fname, params, as_var = nodes

    value = {
        'action': 'call_integration',
        'integration': integration,
        'function': fname,
        'function_params': params
    }

    if as_var is not None:
        _, variable_name = as_var
        set_var_action = {
            'action': 'set_var',
            'var_name': variable_name,
            'value': f'${integration}.{fname}'
        }
        return [value, set_var_action]

    return value


def attribute_value(_, nodes):
    """
    ATTRIBUTE: 'set' IDENTIFIER IDENTIFIER
    """
    return nodes[1], nodes[2]


def card_body_value(context, nodes):
    """
    CARD_BODY: ATTRIBUTE+[SEPARATOR] BUTTON_DEFINITION*[SEPARATOR];
    """
    attributes, buttons = nodes[0], nodes[1]

    card_body = {name: value for name, value in attributes}
    if not card_body.get('title'):
        raise CardTitleEmptyError(
            ErrorContext(
                _script.get_current_file(),
                context
            )
        )
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
    _script.add_component(
        context,
        ComponentType.CAROUSEL,
        identifier,
        carousel_body
    )


def carousel_content_source_value(_, nodes):
    """
    CAROUSEL_CONTENT_SOURCE: 'using' EXPRESSION;
    """
    return nodes[1]


def show_component_value(context, nodes):
    """
    SHOW_COMPONENT: 'show' IDENTIFIER ['using' EXPRESSION];
    """
    _, name, source = nodes

    if _script.has_component(ComponentType.CAROUSEL, name):
        return send_carousel_value(context, name, source)
    elif _script.has_component(ComponentType.MENU, name):
        return send_menu_value(context, name, source)

    raise UndefinedComponent(
        ErrorContext(
            _script.get_current_file(),
            context
        ),
        name
    )


def send_carousel_value(context, name, source):
    carousel, _ = _script.get_component(context, ComponentType.CAROUSEL, name)
    send_carousel = {'action': 'send_carousel'}
    send_carousel.update(carousel)

    if 'card_content' in carousel:
        if not source:
            raise DynamicCarouselMissingSource(
                ErrorContext(
                    _script.get_current_file(),
                    context
                ),
                name
            )

        send_carousel.update({'content_source': source})

    elif source:
        raise StaticCarouselWithSource(
            ErrorContext(
                _script.get_current_file(),
                context
            ),
            name
        )

    return send_carousel


def send_menu_value(context, name, source):
    menu, _ = _script.get_component(context, ComponentType.MENU, name)
    menu['action'] = 'send_menu'
    if source:
        menu['buttons'] = source
    elif 'buttons' not in menu:  # Trying to display an empty menu
        raise EmptyMenuMissingSource(
            ErrorContext(
                _script.get_current_file(),
                context
            ),
            name
        )

    return menu


def set_var_value(context, nodes):
    """
    SET_VAR: 'var' OBJECT '=' E;
    """
    _, object_, _, exp = nodes

    set_var = {
        'action': 'set_var',
        'var_name': object_,
        'value': get_expression_value(exp)
    }

    return set_var


def single_action_value(context, nodes):
    """
    SINGLE_ACTION: COLON ACTION;
    """
    return [nodes[1]]


def scalar_button_value(_, nodes):
    """
    SCALAR_BUTTON: SCALAR_BUTTON_TYPE OPEN STRING SEPARATOR STRING CLOSE;
    """
    button_type, label, payload = nodes[0], nodes[2], nodes[4]

    if button_type == 'url':
        return {
            'label': label,
            'payload': payload,
            'type': 'open_url'
        }
    elif button_type == 'message':
        return {
            'label': label,
            'payload': payload,
            'type': 'message'
        }


def postback_attribute_value(_, nodes):
    """
    POSTBACK_ATTRIBUTE: IDENTIFIER COLON STRING;
    """
    return nodes[0], nodes[2]


def postback_button_value(_, nodes):
    """
    POSTBACK_BUTTON: 'postback' OPEN
        STRING SEPARATOR POSTBACK_PARAMS
    CLOSE;
    """
    label, attributes = nodes[2], nodes[4]

    if isinstance(attributes, list):
        payload = {}
        for key, name in attributes:
            payload.update({key: name})
    else:
        payload = attributes

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


def build_flows() -> list:
    try:
        flows = _script.get_components_by_type(ComponentType.FLOW)
        onboarding = flows.pop('onboarding')
        flows = [onboarding] + list(flows.values())
    except KeyError:
        flows = list(flows.values())

    return [flow for flow, _ in flows]


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
        'COMMAND': define_command_value,
        'COMMENT': pass_none,
        'CONSTANT': constant_value,
        'DEFINITION': definition_value,
        'ELSE': else_value,
        'ELSE_BODY': else_body_value,
        'ENTITY': prefixed_value,
        'EQUALS': equals_value,
        'EXAMPLE_FILE': example_file_value,
        'EXAMPLE_LIST': example_list_value,
        'FALLBACK': fallback_value,
        'FLOW': flow_value,
        'FLOW_type': flow_type_value,
        'HAS_ENTITY': has_entity_value,
        'IF': if_statement_value,
        'IF_BODY': if_body_value,
        'INTEGER': integer_value,
        'INTENT': prefixed_value,
        'IS_EMPTY': is_empty_value,
        'LITERAL_OBJECT': literal_object_value,
        'MEMBER': prefixed_value,
        'MEMBER_DEFINITION': member_definiiton_value,
        'MENU': define_menu_value,
        'OBJECT': object_value,
        'OPEN_FLOW': open_flow_value,
        'OPERATOR': operator_value,
        'PARAMETERS': parameters_value,
        'POSTBACK_ATTRIBUTE': postback_attribute_value,
        'POSTBACK_BUTTON': postback_button_value,
        'QUICK_REPLIES': quick_replies_value,
        'REPLY': reply_value,
        'REPLY_BODY': reply_body_value,
        'SCALAR_BUTTON': scalar_button_value,
        'SET_VAR': set_var_value,
        'SET_ARRAY': set_var_value,
        'SHOW_COMPONENT': show_component_value,
        'SINGLE_ACTION': single_action_value,
        'STRING': string_value,
        'SUBSCRIBE_FEED': subscribe_feed_value,
        'UNSUBSCRIBE_FEED': unsubscribe_feed_value,
        'VARIABLE': prefixed_value,
    }


def set_script(script):
    global _script
    _script = script
