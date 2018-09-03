import os
from enum import Enum

import parglare

__home__ = os.path.abspath(os.path.dirname(__file__))


class OutputVersion(Enum):
    V20 = 'v2.0.0'
    V21 = 'v2.1.0'


def asset_path(asset: str) -> str:
    return os.path.join(__home__, 'assets', asset)


def get_boolean_environ(variable_name):
    return False if os.environ.get(variable_name) in ('', None) else True


def get_position_from_context(context):
    return parglare.pos_to_line_col(context.input_str, context.start_position)
