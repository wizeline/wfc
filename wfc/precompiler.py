import os
import re


def remove_comment(line):
    return re.sub('^[^\'\"]*--.*$', '', line)


def include_file(context: object, line: str) -> None:
    line = line.rstrip()
    input_path = os.path.join(context.get_work_directory(),
                              line.split(' ')[1] + '.flow')
    context.add_input_file(input_path)


def pre_compile(context: object, source: str) -> str:
    buf = []
    for line in source.split('\n'):
        if line.startswith('%include'):
            include_file(context, line)
            buf.append('\n')
        else:
            buf.append(remove_comment(line))

    return '\n'.join(buf)
