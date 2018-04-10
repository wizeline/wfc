import sys
import os

from parglare.exceptions import ParseError

from wfc import output
from wfc.commons import asset_path
from wfc.errors import CompilationError, WFCError
from wfc.parser import create_parser
from wfc.precompiler import pre_compile


def compile(**kwargs):
    """Compiles a Flow script into the selected output format

    Keyword Arguments:
    in_script -- input file. sys.stdin by default
    out_script -- output file. sys.stdout by default
    out_format -- script output format. 'v1' by default
    work_dir -- work directory. '.' by default
    quiet -- suppress standard error. False by default
    """
    in_script = kwargs.get('in_script', sys.stdin)
    out_script = kwargs.get('out_script', sys.stdout)
    out_format = kwargs.get('format_source', 'v1')
    work_dir = kwargs.get('work_dir', os.path.abspath(os.path.curdir))
    quiet = kwargs.get('quiet', False)

    compiled_script = None

    try:
        in_script = in_script.read()
        compiled_script = compile_string(in_script, out_format, work_dir)
        out_script.write(compiled_script)

    except ParseError as ex:
        if not quiet:
            dump_script(in_script, ex)
        raise CompilationError(str(ex))

    except WFCError as e:
        if compiled_script:
            with open('failed.json', 'w') as wfcout:
                wfcout.write(compiled_script)
        raise e


def compile_string(in_script, out_format='v1', work_dir=os.curdir):
    in_script = pre_compile(work_dir, in_script)
    parser = create_parser(asset_path('grammar.txt'),
                           output.build_actions(out_format))
    parser.parse(in_script)
    return output.get_script(out_format)


def dump_script(script, parse_error):
    for ln, line in enumerate(script.split('\n'), 1):
        sys.stderr.write('\n{:>6}  {}'.format(ln, line))
        if ln == parse_error.line:
            sys.stderr.write('\n' + ' ' * (8 + parse_error.column) + '^')
    sys.stderr.write('\n{}\n'.format(parse_error))
