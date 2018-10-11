import json

import jsonschema

from jsonschema.exceptions import ValidationError

from wfc.commons import load_output_schema
from wfc.errors import CompilationError, UnusedIntent
from wfc.output import rules
from wfc.types import ComponentType

_script = None


def build_actions() -> dict:
    return rules.build_actions()


def build_commands() -> list:
    commands = []
    registered_commands = _script.get_components_by_type(
        ComponentType.COMMAND
    ).values()

    for command in registered_commands:
        if not _script.has_component(ComponentType.FLOW, command['dialog']):
            raise CompilationError(
                None,
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
    for intent in registered_intents:
        if 'dialog' not in intent:
            raise UnusedIntent(
                None,
                _script.compiler_context.get_input_path(),
                'Intent not used: {}'.format(intent['name'])
            )
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
        script = {
            'version': "2.0.0",
            'intentions': build_intentions(),
            'entities': [],
            'dialogs': build_flows(),
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
    rules.set_script(script)
