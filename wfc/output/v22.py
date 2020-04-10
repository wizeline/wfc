import json

from wfc.errors import (
    CompilationError,
    ErrorContext,
    WaitInputWithQuickReplies
)
from wfc.output import rules
from wfc.schema import SchemaValidator
from wfc.types import ComponentType

_script = None


def quick_replies_value(context, nodes):
    replies, fallback = nodes[2]

    entities = []
    expect = {}
    the_replies = []

    for text, entity in replies:
        if text is not None:
            the_replies.append(text)
        if entity is not None:
            entities.append(entity[1:])  # <@entity> becomes <entity>

    quick_replies = {
        'replies': the_replies
    }

    if entities:
        expect['fallback'] = fallback
        expect['entities'] = entities

    return quick_replies, expect


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

        if quick_replies['replies']:
            raise WaitInputWithQuickReplies(ErrorContext(
                _script.get_current_file(),
                context
            ))

        if expect:
            value['expect'] = expect

    if context_switch:
        value['can_switch_context'] = False

    return value


def build_actions():
    actions = rules.build_actions()
    actions.update({
        'BOT_WAITS': bot_waits_value,
        'QUICK_REPLIES': quick_replies_value
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
        'version': '2.2.0',
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
