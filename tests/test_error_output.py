import os
import sys
import unittest

from wfc import cli
from tests import SAMPLES_HOME
from tests.util import mixins


class TestErrorOutput(unittest.TestCase, mixins.SampleHandler):
    def setUp(self):
        self.maxDiff = None
        self.output = '/tmp/errors.txt'
        self.stderr = sys.stderr

    def tearDown(self):
        sys.stderr = self.stderr

    def try_to_compile(self, *flows):
        with open(self.output, 'w') as output:
            sys.stderr = output
            sys.argv = [
                'wfc',
                '-w', SAMPLES_HOME,
                ' '.join(flows)
            ]
            cli.main()

    def load_output(self):
        with open(self.output) as output:
            return output.read()

    def load_expected_output(self, file_name):
        with open(os.path.join(SAMPLES_HOME, file_name)) as output:
            return output.read()

    def run_test(self, error_file, *modules):
        self.try_to_compile(*modules)
        with self.load_sample(error_file) as expected_error:
            self.assertEquals(
                expected_error.read(),
                self.load_output()
            )

    def test_ask_bad_syntax(self):
        self.run_test('ask-bad-syntax.err',
                      'ask-bad-syntax.flow')

    def test_call_function_with_bad_syntax(self):
        self.run_test('call-function-bad-syntax.err',
                      'call-function-bad-syntax.flow')

    def test_change_flow_with_bad_syntax(self):
        self.run_test('change-flow-bad-syntax.err',
                      'change-flow-bad-syntax.flow')

    def test_change_unexisting_flow(self):
        self.run_test('change-unexisting-flow.err',
                      'change-unexisting-flow.flow')

    def test_commands_with_bad_syntax(self):
        self.run_test('commands-bad-syntax.err',
                      'commands-bad-syntax.flow')

    def test_commands_redefinition(self):
        self.run_test('commands-redefinition.err',
                      'commands-redefinition.flow')

    def test_commands_with_undefined_flow(self):
        self.run_test('commands-with-undefined-flow.err',
                      'commands-with-undefined-flow.flow')

    def test_control_with_bad_syntax(self):
        self.run_test('control-with-bad-syntax.err',
                      'control-with-bad-syntax.flow')

    def test_dynamic_carousel_without_source(self):
        self.run_test('dynamic-carousel-without-source.err',
                      'dynamic-carousel-without-source.flow')

    def test_dynamic_carousel_with_empty_title(self):
        self.run_test('dynamic-carousel-with-empty-title.err',
                      'dynamic-carousel-with-empty-title.flow')

    def test_error(self):
        self.run_test('error.err',
                      'error.flow')

    def test_fallback_flow_bad_syntax(self):
        self.run_test('fallback-flow-bad-syntax.err',
                      'fallback-flow-bad-syntax.flow')

    def test_fallback_flow_redefinition(self):
        self.run_test('fallback-flow-redefinition.err',
                      'fallback-flow-redefinition.flow')

    def test_if_condition_is_not_other(self):
        self.run_test('if-condition-is-not-other.err',
                      'if-condition-is-not-other.flow')

    def test_intent_bad_syntax(self):
        self.run_test('intent-bad-syntax.err',
                      'intent-bad-syntax.flow')

    def test_intent_not_used(self):
        self.run_test('intent-not-used.err',
                      'intent-not-used.flow')

    def test_open_flow_bad_syntax(self):
        self.run_test('open-flow-bad-syntax.err',
                      'open-flow-bad-syntax.flow')

    def test_open_unexisting_flow(self):
        self.run_test('open-unexisting-flow.err',
                      'open-unexisting-flow.flow')

    def test_qna_flow_bad_syntax(self):
        self.run_test('qna-flow-bad-syntax.err',
                      'qna-flow-bad-syntax.flow')

    def test_qna_flow_redefinition(self):
        self.run_test('qna-flow-redefinition.err',
                      'qna-flow-redefinition.flow')

    def test_send_carousel_with_bad_syntax(self):
        self.run_test('send-carousel-with-bad-syntax.err',
                      'send-carousel-with-bad-syntax.flow')

    def test_send_carousel_with_buttons(self):
        self.run_test('send-carousel-with-buttons.err',
                      'send-carousel-with-buttons.flow')

    def test_send_undefined_carousel(self):
        self.run_test('send-undefined-carousel.err',
                      'send-undefined-carousel.flow')

    def test_send_empty_menu(self):
        self.run_test('send-empty-menu.err',
                      'send-empty-menu.flow')

    def test_static_carousel_with_source(self):
        self.run_test('static-carousel-with-source.err',
                      'static-carousel-with-source.flow')

    def test_subscription_with_bad_syntax(self):
        self.run_test('subscription-with-bad-syntax.err',
                      'subscription-with-bad-syntax.flow')

    def test_var_bad_syntax(self):
        self.run_test('var-bad-syntax.err',
                      'var-bad-syntax.flow')

    def test_wait_to_set_a_constant(self):
        self.run_test('wait-to-set-constant.err',
                      'wait-to-set-constant.flow')

    def test_wait_with_quick_replies1(self):
        self.run_test('wait-with-quick-replies1.err',
                      'wait-with-quick-replies1.flow')

    def test_wait_with_quick_replies2(self):
        self.run_test('wait-with-quick-replies2.err',
                      'wait-with-quick-replies2.flow')

    def test_wait_with_quick_replies3(self):
        self.run_test('wait-with-quick-replies3.err',
                      'wait-with-quick-replies3.flow')

    def test_handoff_without_arguments(self):
        self.run_test('handoff-without-arguments.err',
                      'handoff-without-arguments.flow')
