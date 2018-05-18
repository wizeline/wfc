from parglare import Grammar, Parser

from wfc.commons import get_boolean_environ


def create_parser(grammar_path, actions):
    return Parser(
        Grammar.from_file(grammar_path),
        debug=get_boolean_environ('DEBUG'),
        debug_layout=get_boolean_environ('DEBUG_LEVEL'),
        actions=actions
    )
