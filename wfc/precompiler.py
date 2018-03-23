import os
import re


def remove_comment(line):
    return re.sub('--.*$', '', line)


def include_file(work_dir, line):
    try:
        lines = []
        line = line.rstrip()
        input_path = os.path.join(work_dir, line.split(' ')[1] + '.flow')

        with open(input_path) as input_file:
            for line in input_file.readlines():
                lines.append(remove_comment(line))
            return lines

    except TypeError as e:
        print('[{}] [{}]'.format(work_dir, line))
        raise e


def pre_compile(work_dir, source):
    buf = []
    for line in source.readlines():
        if line.startswith('%include'):
            buf.extend(include_file(work_dir, line))
        else:
            buf.append(remove_comment(line))

    return ''.join(buf)
