import os
import sys

from wfc import core

from tests import CompilerTestCase


class TestContext(CompilerTestCase):
    def test_create_context_with_bad_workdirectory(self):
        args = self.arg_parser.parse_args([
            '-w', 'not-a-directory'
        ])
        with self.assertRaises(FileNotFoundError):
            core.CompilerContext(args)

    def test_create_context_with_bad_not_a_directory(self):
        args = self.arg_parser.parse_args([
            '-w', __file__
        ])
        with self.assertRaises(NotADirectoryError):
            core.CompilerContext(args)

    def test_create_context_with_no_arguments(self):
        args = self.arg_parser.parse_args([])
        with core.CompilerContext(args) as context:
            self.assertIs(sys.stdout, context.get_output_file())
            self.assertIs(sys.stdin, context.get_input_file())
            self.assertEqual('2.1.0', context.get_output_version())
            self.assertEqual(os.path.abspath('.'),
                             context.get_work_directory())
            self.assertTrue(context.is_verbose())

            self.assertTrue(context.has_pending_sources())
            context.next()
            self.assertFalse(context.has_pending_sources())
