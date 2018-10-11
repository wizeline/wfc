import sys

from uuid import uuid4

import yaml
import jsonschema

from jsonschema.exceptions import ValidationError

from wfc.commons import load_output_schema
from wfc.errors import CompilationError
from wfc.output import rules
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


def bot_asks_value(_, nodes):
    bot_asks = rules.bot_asks_value(_, nodes)
    # TODO: Disabling context switching has a bug for script v2.1.0, the fix is
    # coming soon. Meanwhile we just remove the option
    bot_asks.pop('can_switch_context', None)
    return bot_asks


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


def send_carousel_value(context, nodes):
    carousel = rules.send_carousel_value(context, nodes)
    if 'cards' in carousel:
        carousel.update({'action': 'send_static_carousel'})
    elif 'card_content' in carousel:
        carousel.update({'action': 'send_dynamic_carousel'})
    else:
        raise CompilationError(context, 'invalid carousel')

    return carousel


def build_actions() -> dict:
    actions = rules.build_actions()
    actions.update({
        'ACTION': action_value,
        'BOT_ASKS': bot_asks_value,
        'CHANGE_FLOW': change_flow_value,
        'IF': if_statement_value,
        'SEND_CAROUSEL': send_carousel_value
    })
    return actions


def build_commands() -> list:
    commands = []

    for command in _script.get_components_by_type(ComponentType.COMMAND).values():
        if not _script.has_component(ComponentType.FLOW, command['dialog']):
            raise CompilationError(
                None,
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
    for intent in _script.get_components_by_type(ComponentType.INTENT).values():
        if 'dialog' not in intent:
            raise CompilationError(
                None,
                'Intent not used: {}'.format(intent['name'])
            )

        flow = intent.pop('dialog')
        intent['flow'] = flow

        intent.pop('examples')

        intents.append(intent)
    return intents


def build_flows() -> list:
    try:
        flows = _script.get_components_by_type(ComponentType.FLOW)
        onboarding = flows.pop('onboarding')
        flows = [onboarding] + list(flows.values())
    except KeyError:
        flows = list(flows.values())

    return flows


def get_script():
    _script.perform_sanity_checks()
    try:
        pass
        script = {
            'version': '2.1.0',
            'flows': build_flows(),
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

        jsonschema.validate(script, load_output_schema('2.1.0'))
        return yaml.dump(script, default_flow_style=False)
    except ValidationError as ex:
        with open('/tmp/invalid.yaml', 'w') as invalid_script:
            dumped_script = yaml.dump(script, default_flow_style=False)
            invalid_script.write(dumped_script)

        sys.stderr.write(dumped_script)
        raise ValueError('Generated script does not match with schema')


def set_script(script):
    global _script
    _script = script
    rules.set_script(script)
