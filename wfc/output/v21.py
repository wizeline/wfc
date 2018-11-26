from uuid import uuid4

import yaml

from wfc.errors import CompilationError
from wfc.output import rules
from wfc.schema import SchemaValidator
from wfc.types import ComponentType

_script = None


def action_value(_, nodes):
    action_body = nodes[0]
    action_name = action_body.pop('action')
    action = {
        action_name: action_body
    }
    action['id'] = str(uuid4())
    return action


def change_flow_value(_, nodes):
    change_flow = rules.change_flow_value(_, nodes)
    flow_name = change_flow.pop('dialog')
    change_flow.update({
        'action': 'change_flow',
        'flow': flow_name
    })
    return change_flow


def get_action_name(action):
    return (set(action) - {'id'}).pop()


def if_statement_value(_, nodes):
    """
    if CONDITION IF_BODY
    """
    _, condition, if_body = nodes
    actions, else_actions = if_body
    for action in actions:
        name = get_action_name(action)
        action[name]['condition'] = condition

    if else_actions not in (None, 'end'):
        negative = rules.not_condition(condition)
        for else_action in else_actions:
            name = get_action_name(action)
            else_action[name]['condition'] = negative
        actions += else_actions

    return actions


def show_component_value(context, nodes):
    component = rules.show_component_value(context, nodes)
    if 'cards' in component:
        component.update({'action': 'send_static_carousel'})
    elif 'card_content' in component:
        component.update({'action': 'send_dynamic_carousel'})

    return component


def build_actions() -> dict:
    actions = rules.build_actions()
    actions.update({
        'ACTION': action_value,
        'CHANGE_FLOW': change_flow_value,
        'IF': if_statement_value,
        'SHOW_COMPONENT': show_component_value
    })
    return actions


def build_commands() -> list:
    commands = []
    registered_commands = _script.get_components_by_type(
        ComponentType.COMMAND
    ).values()

    for command, definition_context in registered_commands:
        if not _script.has_component(ComponentType.FLOW, command['dialog']):
            raise CompilationError(
                definition_context,
                'Command linked to unexisting flow: {} -> {}'.format(
                    command['keyword'],
                    command['dialog']
                )
            )
        flow = command.pop('dialog')
        command['flow'] = flow
        commands.append(command)

    return commands


def build_intentions() -> list:
    intents = []
    registered_intents = _script.get_components_by_type(
        ComponentType.INTENT
    ).values()
    for intent, definition_context in registered_intents:
        if 'dialog' not in intent:
            raise CompilationError(
                definition_context,
                'Intent not used: {}'.format(intent['name'])
            )

        flow = intent.pop('dialog')
        intent['flow'] = flow

        intent.pop('examples')

        intents.append(intent)
    return intents


def get_script():
    _script.perform_sanity_checks()
    pass
    script = {
        'version': '2.1.0',
        'flows': rules.build_flows(),
    }

    intentions = build_intentions()
    if intentions:
        script.update({'intents': intentions})

    commands = build_commands()
    if commands:
        script.update({'commands': commands})

    fallback_flow = _script.get_fallback_flow()
    if fallback_flow:
        script['nlp_fallback'] = fallback_flow

    qna_flow = _script.get_qna_flow()
    if qna_flow:
        script['qna_followup'] = qna_flow

    SchemaValidator().execute(script)
    return yaml.dump(script, default_flow_style=False)


def set_script(script):
    global _script
    _script = script
    rules.set_script(script)
