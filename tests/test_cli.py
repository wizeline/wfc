import errno
import os
import sys

from wfc import cli
from tests import CompilerTestCase, SAMPLES_HOME


class TestMain(CompilerTestCase):
    def setUp(self):
        super().setUp()
        self._stderr = sys.stderr
        sys.stderr = self.open_tmpout()

    def tearDown(self):
        super().tearDown()
        sys.stderr = self._stderr

    def test_run_main_with_ghost_workdir(self):
        sys.argv = ['wfc', '-q', '-w', SAMPLES_HOME + '/does-not-exist']
        self.assertEqual(errno.ENOENT, cli.main())

    def test_run_main_with_workdir_not_a_dir(self):
        sys.argv = ['wfc', '-q', '-w', __file__]
        self.assertEqual(errno.ENOTDIR, cli.main())

    def test_run_main_with_several_modules(self):
        sys.argv = ['wfc', '-o', os.path.devnull, '-q', '-w', SAMPLES_HOME,
                    'ask.flow', 'say.flow']
        self.assertEqual(0, cli.main())

    def test_try_to_compile_a_directory(self):
        sys.argv = ['wfc', '-q', SAMPLES_HOME]
        self.assertEqual(errno.EISDIR, cli.main())

    def test_compile_with_syntax_errors(self):
        sys.argv = ['wfc', '-q', '-w', SAMPLES_HOME, 'ask-bad-syntax.flow']
        self.assertEqual(1, cli.main())


class TestArgumentParser(CompilerTestCase):
    def test_parse_with_all_arguments(self):
        arguments = self.arg_parser.parse_args(['-q', '-o', 'script.yaml',
                                                '-v', 'v2.1.0',
                                                '-w', SAMPLES_HOME,
                                                'main.flow', 'module.flow'])

        self.assertEquals('script.yaml', arguments.output)
        self.assertEquals('v2.1.0', arguments.outversion)
        self.assertEquals(SAMPLES_HOME, arguments.workdir)
        self.assertListEqual(['main.flow', 'module.flow'], arguments.flows)
        self.assertTrue(arguments.quiet)

    def test_parse_without_output_file(self):
        arguments = self.arg_parser.parse_args(['-v', 'v2.0.0',
                                                'main.flow', 'module.flow'])

        self.assertEquals('', arguments.output)
        self.assertEquals('v2.0.0', arguments.outversion)
        self.assertEquals(os.curdir, arguments.workdir)
        self.assertListEqual(['main.flow', 'module.flow'], arguments.flows)

    def test_parse_without_output_format(self):
        arguments = self.arg_parser.parse_args(['-o', 'script.json',
                                                'main.flow', 'module.flow'])

        self.assertEquals('script.json', arguments.output)
        self.assertEquals('v2.0.0', arguments.outversion)
        self.assertEquals(os.curdir, arguments.workdir)
        self.assertListEqual(['main.flow', 'module.flow'], arguments.flows)

    def test_parse_with_modules_only(self):
        arguments = self.arg_parser.parse_args(['main.flow', 'module.flow'])

        self.assertEquals('', arguments.output)
        self.assertEquals('v2.0.0', arguments.outversion)
        self.assertEquals(os.curdir, arguments.workdir)
        self.assertListEqual(['main.flow', 'module.flow'], arguments.flows)

    def test_parse_arguments_with_quiet_mode_only(self):
        arguments = self.arg_parser.parse_args(['-q'])

        self.assertEquals('', arguments.output)
        self.assertEquals('v2.0.0', arguments.outversion)
        self.assertListEqual([], arguments.flows)
        self.assertEquals(os.curdir, arguments.workdir)
        self.assertTrue(arguments.quiet)
