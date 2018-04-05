import json
import sys
import os

import jsonschema

from parglare.exceptions import ParseError

from . import Flow, WFCHOME
from .precompiler import pre_compile


class CompilationError(Exception): pass  # noqa


def build_intentions():
    intents = []
    for intent in Flow.INTENTIONS.values():
        if 'dialog' not in intent:
            raise Exception('Intent not used: {}'.format(intent['name']))
        intents.append(intent)
    return intents


def build_dialogs():
    try:
        onboarding = Flow.DIALOGS.pop('onboarding')
        dialogs = [onboarding] + list(Flow.DIALOGS.values())
    except KeyError:
        dialogs = list(Flow.DIALOGS.values())

    return dialogs


def dump_script(script):
    for ln, line in enumerate(script.split('\n'), 1):
        print("%6d  %s" % (ln, line))


def compile_source(parser, work_dir, source, output=sys.stdout):
    Flow.DIALOGS = {}
    Flow.ENTITIES = {}
    Flow.INTENTIONS = {}

    try:
        script = pre_compile(work_dir, source)
        parser.parse(script)
    except ParseError as ex:
        print(ex)
        print('Dialogs so far:', json.dumps(Flow.DIALOGS, indent=2))
        dump_script(script)
        raise ex

    flow = {
        'version': "1.0.0",
        'intentions': build_intentions(),
        'entities': [],
        'dialogs': build_dialogs(),
        'qa': []
    }

    try:
        # TODO: The `id` field is not currently accepted for send_carousel
        # action, so schema validation will be disabled by now.
        # jsonschema.validate(flow, load_output_schema())
        output.write(json.dumps(flow, indent=2))
    except Exception as e:
        with open('failed.json', 'w') as wfcerror:
            wfcerror.write(json.dumps(flow, indent=2))
        raise e


def load_output_schema():
    with open(os.path.join(WFCHOME, 'assets/schema.json')) as schema:
        return json.loads(schema.read())
