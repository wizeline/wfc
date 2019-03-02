from tests import CompilerTestCase


class TestSubscription(CompilerTestCase):
    def test_subscription_success(self):
        self._compile('subscription')
