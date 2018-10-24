import json

from wfc.errors import CompilationError, UnusedIntent
from wfc.output import rules
from wfc.schema import SchemaValidator
from wfc.types import ComponentType

_script = None


def build_actions() -> dict:
    return rules.build_actions()


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
        commands.append(command)

    return commands


def build_intentions() -> list:
    intents = []
    registered_intents = _script.get_components_by_type(
        ComponentType.INTENT
    ).values()
    for intent, definition_context in registered_intents:
        if 'dialog' not in intent:
            raise UnusedIntent(definition_context, intent['name'])
        intents.append(intent)
    return intents


def get_script():
    _script.perform_sanity_checks()
    script = {
        'version': "2.0.0",
        'intentions': build_intentions(),
        'entities': [],
        'dialogs': rules.build_flows(),
        'qa': []
    }
    commands = build_commands()
    if commands:
        script['commands'] = commands

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
