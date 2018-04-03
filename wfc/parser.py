import os

from parglare import Grammar, Parser

from . import WFCHOME
from .actions.v1 import build_actions


def load_grammar():
    grammar_path = os.path.join(WFCHOME, 'assets/grammar.txt')
    return Grammar.from_file(grammar_path)


def create_parser():
    debug_level = False if os.environ.get('DEBUG') in ('', None) else True
    return Parser(load_grammar(), debug=debug_level, actions=build_actions())
