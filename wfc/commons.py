import json
import os

import parglare

from wfc.types import OutputVersion

__home__ = os.path.abspath(os.path.dirname(__file__))


def asset_path(asset: str) -> str:
    return os.path.join(__home__, 'assets', asset)


def get_boolean_environ(variable_name):
    return False if os.environ.get(variable_name) in ('', None) else True


def get_position_from_context(context):
    return parglare.pos_to_line_col(context.input_str, context.start_position)


def load_output_schema(version_name='2.1.0') -> dict:
    version = OutputVersion(version_name)
    if version == OutputVersion.V21:
        schema_file = 'schema21.json'
    elif version == OutputVersion.V20:
        schema_file = 'schema.json'
    else:
        raise ValueError('Invalid schema', version)

    with open(asset_path(schema_file)) as schema:
        return json.loads(schema.read())
