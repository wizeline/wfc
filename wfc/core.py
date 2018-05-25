import errno
import sys
import os

from parglare.exceptions import ParseError as ParglareParseError

from wfc import output
from wfc.commons import asset_path
from wfc.errors import CompilationError, ParseError, WFCError
from wfc.parser import create_parser
from wfc.precompiler import pre_compile


class CompilerContext:
    def __init__(self, args=None):
        self._current_source = 0
        self._output_file = None

        if args is None:
            self._flow_paths = [None]
            self._output_path = None
            self._output_version = 'v1'
            self._verbose = True
            self._work_dir = os.path.abspath(os.curdir)
        else:
            self._work_dir = os.path.abspath(args.workdir)
            if not os.path.exists(self._work_dir):
                raise FileNotFoundError(
                    errno.ENOENT,
                    "Work directory not found: '{}'".format(self._work_dir)
                )

            if not os.path.isdir(self._work_dir):
                raise NotADirectoryError(
                    errno.ENOTDIR,
                    "Not a directory: '{}'".format(self._work_dir)
                )

            self._output_path = args.output
            self._output_version = args.outversion
            self._verbose = not args.quiet
            self._flow_paths = [
                os.path.join(self._work_dir, flow) for flow in args.flows
            ]

        self._script = output.Script()
        self._output = output.OutputBuilder(self._script, self._output_version)
        self._parser = create_parser(asset_path('grammar.txt'),
                                     self._output.get_actions())

    def __enter__(self):
        if self._flow_paths == [None]:
            self._flow_files = [sys.stdin]
        else:
            self._flow_files = [open(flow) for flow in self._flow_paths]

        if self._output_path:
            self._output_file = open(self._output_path, 'w')
        else:
            self._output_file = sys.stdout

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if sys.stdin not in self._flow_files:
            for flow in self._flow_files:
                flow.close()

        if sys.stdout is not self._output_file:
            self._output_file.close()

    def add_input_file(self, input_path):
        if not input_path in self._flow_paths:
            self._flow_paths.append(input_path)
            self._flow_files.append(open(input_path))

    def build_script(self):
        return self._output.get_script()

    def has_pending_sources(self):
        return self._current_source < len(self._flow_files)

    def next(self):
        self._current_source += 1

    def get_input_file(self):
        return self._flow_files[self._current_source]

    def get_input_path(self):
        return self._flow_paths[self._current_source] or 'STDIN'

    def get_output_file(self):
        return self._output_file or sys.stdout

    def get_output_version(self):
        return self._output_version

    def get_parser(self):
        return self._parser

    def get_work_directory(self):
        return self._work_dir

    def is_verbose(self):
        return self._verbose

    def set_quiet(self):
        self._verbose = False

    def set_verbose(self):
        self._verbose = True


def compile(context):
    """Compiles a Flow script into the selected output format"""

    verbose = context.is_verbose()

    while context.has_pending_sources():
        try:
            in_script = context.get_input_file().read()
            compile_string(context, in_script)
            context.next()
        except (CompilationError, WFCError) as error:
            if verbose:
                dump_script(context, in_script, error)
            return 1

    try:
        out_file = context.get_output_file()
        out_file.write(context.build_script())
    except CompilationError as error:
        if verbose:
            sys.stderr.write(str(error))
        return 2

    return 0


def compile_string(context, in_script):
    parser = context.get_parser()

    in_script = pre_compile(context, in_script)
    try:
        parser.parse(in_script)
    except ParglareParseError as ex:
        raise ParseError(ex)


def dump_script(context, script, parse_error):
    input_path = os.path.basename(context.get_input_path())
    sys.stderr.write('{}|{}\n'.format(input_path, str(parse_error)))
    start, end = get_dump_frame(parse_error)
    script_lines = get_script_frame(script, start, end)

    for ln, line in enumerate(script_lines, start + 1):
        sys.stderr.write('{:>6}  {}\n'.format(ln, line))
        if ln == parse_error.context.line:
            hfill = ' ' * (8 + parse_error.context.column)
            sys.stderr.write('{}^\n'.format(hfill))


def get_dump_frame(parse_error):
    start, end = parse_error.context.line - 5, parse_error.context.line + 5
    if start < 0:
        start = 0

    return start, end


def get_script_frame(script, start, end):
    return script.split('\n')[start:end]
