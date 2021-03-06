import json

from wfc.errors import CompilationError
from wfc.output import rules
from wfc.schema import SchemaValidator
from wfc.types import ComponentType

_script = None


def handoff_value(context, nodes):
    """
    'HANDOFF_ACTION HANDOFF_ARGUMENT+'

    Note: script version 2.1 only accepts one argument: assignee, so the other
    arguments are ignored
    """
    handoff = rules.handoff_value(context, nodes)

    if 'user_info' in handoff:
        handoff.pop('user_info')

    return handoff


def build_actions():
    actions = rules.build_actions()
    actions.update({
        'HANDOFF_ACTION': handoff_value
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
    return json.dumps(script, indent=2)


def set_script(script):
    global _script
    _script = script
    rules.set_script(script)
