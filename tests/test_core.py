import os
import sys

from wfc import core

from tests import CompilerTestCase


class TestCore(CompilerTestCase):
    def _test_send_media_success(self):
        # self._compile_to_json('send-media')
        pass

    def _test_send_menu_success(self):
        # self._compile_to_json('send-menu')
        pass

    def _test_open_flow(self):
        # Action not implemented
        # self._compile_to_json('send-menu')
        pass


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
        with core.CompilerContext(None) as context:
            self.assertIs(sys.stdout, context.get_output_file())
            self.assertIs(sys.stdin, context.get_input_file())
            self.assertEqual('v2', context.get_output_version())
            self.assertEqual(os.path.abspath('.'),
                             context.get_work_directory())
            self.assertTrue(context.is_verbose())

            self.assertTrue(context.has_pending_sources())
            context.next()
            self.assertFalse(context.has_pending_sources())
