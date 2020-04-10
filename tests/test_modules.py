import json
import os

from tests import CompilerTestCase, SAMPLES_HOME


class TestModules(CompilerTestCase):
    def setUp(self):
        super().setUp()

    def test_compile_several_modules(self):
        rc = self._compile_with_args([
            '-o',
            self.get_tmp_path(),
            '-w',
            SAMPLES_HOME,
            'module.flow',
            'root.flow'
        ])
        assert rc == 0, 'Compilation should pass: rc=[{}]'.format(rc)

        with self.open_tmpin() as compiled_script:
            expected = self.load_json_script('root-220.json')
            compiled = json.load(compiled_script)
            self._prune_action_ids(compiled)
            self.assertDictEqual(expected, compiled)

    def test_compile_with_missing_modules(self):
        rc = self._compile_with_args([
            '-o',
            os.path.devnull,
            '-w',
            SAMPLES_HOME,
            'root.flow'
        ])
        assert rc != 0, 'Compilation should fail'
