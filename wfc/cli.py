#!/usr/bin/env python3
import json
import os
import sys

from argparse import ArgumentParser

from wfc import core, get_version
from wfc.commons import OutputVersion
from wfc.errors import InvalidOutputFormat, SchemaViolationError
from wfc.schema import SchemaValidator


def main():
    argument_parser = make_argument_parser()
    args = argument_parser.parse_args()

    if args.version:
        print(f'wfc {get_version()}')
        return 0

    try:
        if args.check_schema:
            validator = SchemaValidator()
            for script_file_name in args.check_schema:
                with open(script_file_name) as script_file:
                    validator.execute(json.load(script_file))
            return 0

        else:
            with core.CompilerContext(args) as context:
                rc = core.compile(context)
    except (
        FileNotFoundError,
        IsADirectoryError,
        NotADirectoryError,
        InvalidOutputFormat,
        SchemaViolationError
    ) as ex:
        sys.stderr.write(f'{ex}\n')
        rc = getattr(ex, 'errno', 1)

    return rc


MAIN_HELP = ('Compiles chatbot scripts written in flow language into'
             'JSON or YAML format.')


def make_argument_parser():
    parser = ArgumentParser(
        prog='wfc',
        description=MAIN_HELP
    )
    parser.add_argument('-V', '--version', default=False, action='store_true')
    parser.add_argument('flows', metavar='flow', type=str, nargs='*',
                        default=[None], help='input .flow files')
    parser.add_argument('-o', '--output', default='', help='output file')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='run compiler in quiet mode')
    parser.add_argument('-v', '--outversion', default=OutputVersion.V20.value,
                        help='Output format: "2.0.0", "2.1.0"')
    parser.add_argument('-w', '--workdir', default=os.curdir,
                        help='work directory')
    parser.add_argument('--check-schema', nargs='+',
                        help='Validate if compiled script meets schema')

    return parser
