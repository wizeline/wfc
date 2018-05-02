#!/usr/bin/env python3
import os
import sys

from wfc import core
from wfc.errors import CompilationError, WFCError


def main():
    try:
        if len(sys.argv) == 1:
            core.compile()
        else:
            for source in sys.argv[1:]:
                work_dir = os.path.abspath(os.path.dirname(source))
                with open(source) as in_script:
                    core.compile(work_dir=work_dir, in_script=in_script)
        rc = 0
    except (CompilationError, WFCError) as ex:
        sys.stderr.write('\n{}\n'.format(ex))
        rc = 1

    return rc
