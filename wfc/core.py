import sys
import os

from parglare.exceptions import ParseError as ParglareParseError

from wfc import output
from wfc.commons import asset_path
from wfc.errors import CompilationError, ParseError
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
    in_script = kwargs.pop('in_script', sys.stdin)
    out_script = kwargs.pop('out_script', sys.stdout)
    out_format = kwargs.pop('format_source', 'v1')
    work_dir = kwargs.pop('work_dir', os.path.abspath(os.path.curdir))
    quiet = kwargs.pop('quiet', False)

    compiled_script = None

    try:
        in_script = in_script.read()
        compiled_script = compile_string(in_script, out_format, work_dir)
        out_script.write(compiled_script)

    except ParglareParseError as ex:
        error = ParseError(ex)
        if not quiet:
            dump_script(in_script, error)
        raise error

    except CompilationError as ex:
        if compiled_script:
            with open('failed.json', 'w') as wfcout:
                wfcout.write(compiled_script)

        if ex.context and not quiet:
            dump_script(in_script, ex)
        raise ex


def compile_string(in_script, out_format='v1', work_dir=os.curdir):
    in_script = pre_compile(work_dir, in_script)
    parser = create_parser(asset_path('grammar.txt'),
                           output.build_actions(out_format))
    parser.parse(in_script)
    return output.get_script(out_format)


def get_dump_frame(parse_error):
    start, end = parse_error.context.line - 5, parse_error.context.line + 5
    if start < 0:
        start = 0

    return start, end


def dump_script(script, parse_error):
    start, end = get_dump_frame(parse_error)
    script_lines = script.split('\n')[start:end]

    for ln, line in enumerate(script_lines, start + 1):
        sys.stderr.write('\n{:>6}  {}'.format(ln, line))
        if ln == parse_error.context.line:
            sys.stderr.write('\n' + ' ' * (8 + parse_error.context.column) + '^')
