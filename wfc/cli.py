#!/usr/bin/env python3
import os
import sys

from .core import compile_source
from .parser import create_parser


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        work_dir = os.path.abspath(os.path.curdir)
        compile_source(parser, work_dir, sys.stdin)
    else:
        for source in sys.argv[1:]:
            with open(source) as source_file:
                work_dir = os.path.dirname(source)
                compile_source(parser, work_dir, source_file)
