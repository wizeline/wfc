#!/usr/bin/env python3
import os
import sys

from argparse import ArgumentParser

from wfc import core, get_version
from wfc.commons import OutputVersion
from wfc.errors import InvalidOutputFormat


def main():
    if len(sys.argv) == 1:
        args = None
    else:
        argument_parser = make_argument_parser()
        args = argument_parser.parse_args()

    if args.version:
        print(f'wfc {get_version()}')
        return 0

    try:
        with core.CompilerContext(args) as context:
            rc = core.compile(context)
    except (
        FileNotFoundError,
        IsADirectoryError,
        NotADirectoryError,
        InvalidOutputFormat
    ) as ex:
        sys.stderr.write(f'{ex}\n')
        rc = getattr(ex, 'errno', 1)

    return rc


MAIN_HELP = ('Compiles chatbot scripts written in flow language into'
             'YSON or YAML format.')


def make_argument_parser():
    parser = ArgumentParser(
        prog='wfc',
        description=MAIN_HELP
    )
    parser.add_argument('-V', '--version', default=False, action='store_true')
    parser.add_argument('flows', metavar='flow', type=str, nargs='*',
                        help='input .flow files')
    parser.add_argument('-o', '--output', default='', help='output file')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='run compiler in quiet mode')
    parser.add_argument('-v', '--outversion', default=OutputVersion.V20.value,
                        help='Output format: "2.0.0", "2.1.0"')
    parser.add_argument('-w', '--workdir', default=os.curdir,
                        help='work directory')

    return parser
