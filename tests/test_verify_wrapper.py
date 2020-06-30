import os
from unittest import TestCase

from mock import patch

from pact.constants import VERIFIER_PATH
from pact.verify_wrapper import VerifyWrapper, PactException
from pact import verify_wrapper


from subprocess import PIPE, Popen

class VerifyWrapperTestCase(TestCase):
    """ use traceback.print_exception(*result.exc_info) to debug """

    @classmethod
    def setUpClass(cls):
        # In Python 3 Click makes a call to locale to determine how the
        # terminal wants to handle unicode. Because we mock Popen to avoid
        # calling the real verifier, we need to get the actual result of
        # locale to provide it to Click during the test run.
        if os.name == 'nt':
            cls.locale = ''  # pragma: no cover
        else:
            cls.locale = Popen(
                ['locale', '-a'], stdout=PIPE, stderr=PIPE).communicate()[0]

    def setUp(self):
        super(VerifyWrapperTestCase, self).setUp()
        self.addCleanup(patch.stopall)
        self.mock_Popen = patch.object(
            verify_wrapper.subprocess, 'Popen', spec=verify_wrapper.subprocess.Popen,
            stdout=['6 interactions, 0 failures']).start()

        self.mock_Popen.return_value.communicate.return_value = self.locale

        # self.mock_isfile = patch.object(
        #     VerifyWrapper, 'isfile', autospec=True).start()

        self.mock_rerun_command = patch.object(
            VerifyWrapper, 'rerun_command', autospec=True).start()

        self.default_call = [
            './pacts/consumer-provider.json',
            './pacts/consumer-provider2.json',
            '--provider=test_provider',
            '--provider-base-url=http://localhost']

        self.broker_call = [
            '--provider=test_provider',
            '--provider-base-url=http://localhost',
            '--pact-broker-base-url=http://broker',
            '--broker-username=username',
            '--broker-password=pwd']

    def assertProcess(self, *expected):
        self.assertEqual(self.mock_Popen.call_count, 1)
        process_call = self.mock_Popen.mock_calls[0]

        actual = process_call[1][0]
        self.assertEqual(actual[0], VERIFIER_PATH)
        print(actual)
        print(expected)
        self.assertEqual(len(actual), len(expected) + 1)
        self.assertEqual(set(actual[1:]), set(expected))
        self.assertEqual(set(expected), set(actual[1:]))
        self.assertEqual(
            process_call[2]['env']['PACT_INTERACTION_RERUN_COMMAND'],
            self.mock_rerun_command.return_value)

    def test_pact_urls_provided(self):
        self.mock_Popen.return_value.returncode = 0
        wrapper = VerifyWrapper()

        result, output = wrapper.call_verify('./pacts/consumer-provider.json',
                                             './pacts/consumer-provider2.json',
                                             provider='test_provider',
                                             provider_base_url='http://localhost')

        self.assertProcess(*self.default_call)

        self.assertTrue(self.mock_Popen.called)
        self.assertEqual(result, 0)

    def test_pact_urls_or_broker_required(self):
        self.mock_Popen.return_value.returncode = 2
        wrapper = VerifyWrapper()

        with self.assertRaises(PactException) as context:
            wrapper.call_verify(provider='provider', provider_base_url='http://localhost')

        self.assertTrue('Pact urls or Pact broker required' in context.exception.message)

    def test_uses_broker_if_no_pacts_and_provider_required(self):
        self.mock_Popen.return_value.returncode = 0
        wrapper = VerifyWrapper()

        result, output = wrapper.call_verify(provider='test_provider',
                                             provider_base_url='http://localhost',
                                             broker_username='username',
                                             broker_password='pwd',
                                             broker_url='http://broker')

        self.assertProcess(*self.broker_call)

        self.assertTrue(self.mock_Popen.called)
        self.assertEqual(result, 0)

    def test_expand_pact_files(self):
        """todo
        """
        # todo

    def test_missing_pact_files(self):
        """todo
        """
        # todo

    # def test_provider_base_url_is_required(self):
    #     self.mock_Popen.return_value.returncode = 2
    #     wrapper = VerifyWrapper()

    #     result, output = wrapper.call_verify(provider_base_url='test')

    #     self.assertEqual(result, 2)

    #     # self.assertFalse(result)
    #     args, _ = self.mock_Popen.call_args

    #     self.assertIn('--provider-base-url=test', args[0])
    #     self.assertTrue(self.mock_Popen.called)
