from enum import Enum

import yaml

from parglare.actions import pass_none

from wfc.commons import asset_path
from wfc.errors import (
    CompilationError,
    ComponentNotDefined,
    DynamicCarouselMissingSource,
    StaticCarouselWithSource,
    UndefinedCarousel
)
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
    script = {
        'version': '2.1.0',
        'flows': build_flows()
    }
    return yaml.dump(script, default_flow_style=False)


def set_script(script):
    global _script
    _script = script
    rules.set_script(script)
