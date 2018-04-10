from wfc.errors import InvalidOutputFormat
from wfc.output import v1

_FORMATS = {
    'v1': v1
}


class Script:
    def __init__(self):
        self.FLOWS = {}
        self.CAROUSELS = {}
        self.ENTITIES = {}
        self.INTENTIONS = {}
        self.INTEGRATIONS = {}


def get_script(selected_format):
    try:
        return _FORMATS[selected_format].get_script()
    except KeyError:
        raise InvalidOutputFormat(selected_format)


def build_actions(selected_format='v1'):
    try:
        return _FORMATS[selected_format].build_actions(Script())
    except KeyError:
        raise InvalidOutputFormat(selected_format)
