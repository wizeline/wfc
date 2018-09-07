#!/usr/bin/env python3
import os
import sys

from argparse import ArgumentParser

from wfc import core, get_version
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


def make_argument_parser():
    parser = ArgumentParser(
        prog='wfc',
        description='Compiles .flow files into a chatbotscript'
    )
    parser.add_argument('-V', '--version', default=False, action='store_true')
    parser.add_argument('flows', metavar='flow', type=str, nargs='*',
                        help='input .flow files')
    parser.add_argument('-o', '--output', default='', help='output file')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='run compiler in quiet mode')
    parser.add_argument('-v', '--outversion', default='v2',
                        help='output format')
    parser.add_argument('-w', '--workdir', default=os.curdir,
                        help='work directory')

    return parser
