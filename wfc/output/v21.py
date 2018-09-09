import yaml

from wfc.errors import CompilationError
from wfc.output import rules

_script = None


def action_value(_, nodes):
    action_body = nodes[0]
    action_name = action_body.pop('action')
    action = {
        action_name: action_body
    }
    return action


def build_actions() -> dict:
    actions = rules.build_actions()
    actions.update({'ACTION': action_value})
    return actions


def build_commands() -> list:
    commands = []

    for command in _script.get_components_by_type('command').values():
        if not _script.has_component('flow', command['dialog']):
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
    for intent in _script.get_components_by_type('intent').values():
        if 'dialog' not in intent:
            raise CompilationError(
                None,
                'Intent not used: {}'.format(intent['name'])
            )

        flow = intent.pop('dialog')
        intent['flow'] = flow

        if not intent['examples']:
            intent.pop('examples')

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


def get_script():
    _script.perform_sanity_checks()
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

    return yaml.dump(script, default_flow_style=False)


def set_script(script):
    global _script
    _script = script
    rules.set_script(script)
