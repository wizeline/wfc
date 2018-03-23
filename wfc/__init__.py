from os import path

__version__ = '0.1'

FLOW_HOME = path.abspath(path.dirname(__file__))


class Flow:
    DIALOGS = {}
    CAROUSELS = {}
    ENTITIES = {}
    INTENTIONS = {}
    INTEGRATIONS = {}
