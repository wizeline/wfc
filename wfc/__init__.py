from os import path

__author__ = 'wizeline'
__name__ = 'wfc'
__version__ = '0.1'

WFCHOME = path.abspath(path.dirname(__file__))


class Flow:
    DIALOGS = {}
    CAROUSELS = {}
    ENTITIES = {}
    INTENTIONS = {}
    INTEGRATIONS = {}
