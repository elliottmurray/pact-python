from unittest import TestCase
from mock import patch, mock

from pact.verifier import Verifier
from pact.verify_wrapper import VerifyWrapper

PACT_FILE = 'test.pact'

class VerifierTestCase(TestCase):

    def setUp(self):
        super(VerifierTestCase, self).setUp()
        self.addCleanup(patch.stopall)
        self.verifier = Verifier(provider='test_provider',
                                 provider_base_url="http://localhost:8888")

        self.mock_wrapper = patch.object(
            VerifyWrapper, 'call_verify', spec=True).start()

    @patch("pact.verify_wrapper.isfile", return_value=True)
    def test_verifier_with_provider_and_files(self, mock_isfile):
        self.mock_wrapper.return_value = (True, 'some logs')

        output, _ = self.verifier.verify_pacts('path/to/pact1',
                                               'path/to/pact2')

        self.assertTrue(output)
        self.assertEqual(self.mock_wrapper.call_count, 1)
        args, kwargs = self.mock_wrapper.call_args
        self.assertEquals('path/to/pact1', args[0])
        self.assertEquals('path/to/pact2', args[1])
        self.assertDictEqual({'provider': 'test_provider',
                              'provider_base_url': 'http://localhost:8888'},
                             kwargs)

    def test_verifier_with_provider_and_urls(self):
        self.mock_wrapper.return_value = (True, 'some logs')

        output, _ = self.verifier.verify_pacts('http://path/to/pact1',
                                               'http://path/to/pact2')

        self.assertTrue(output)
        self.assertEqual(self.mock_wrapper.call_count, 1)
        args, kwargs = self.mock_wrapper.call_args
        self.assertEquals('http://path/to/pact1', args[0])
        self.assertEquals('http://path/to/pact2', args[1])
        self.assertDictEqual({'provider': 'test_provider',
                              'provider_base_url': 'http://localhost:8888'},
                             kwargs)

    def test_verifier_with_broker(self):
        pact_broker_username = 'broker_username'
        pact_broker_password = 'broker_password'

        self.mock_wrapper.return_value = (True, 'ddf')

        output, _ = self.verifier.verify_with_broker(broker_username=pact_broker_username,
                                                     broker_password=pact_broker_password,
                                                     broker_url='http://broker')

        self.assertTrue(output)

        self.assertEqual(self.mock_wrapper.call_count, 1)
        args, kwargs = self.mock_wrapper.call_args

        self.assertEquals(len(args), 0)
        self.assertDictEqual({
            'provider': 'test_provider',
            'provider_base_url': 'http://localhost:8888',
            'broker_username': pact_broker_username,
            'broker_password': pact_broker_password,
            'broker_url': 'http://broker',
        },
            kwargs)

    @mock.patch("os.path.isfile", mock.MagicMock(return_value=False))
    def test_missing_pact_files(self):
        with self.assertRaises(Exception) as context:
            output, _ = self.verifier.verify_pacts('path/to/pact1',
                                                   'path/to/pact2')

        self.assertTrue("Missing pact files ['path/to/pact1', 'path/to/pact2']" in str(context.exception))

    # def test_provider_base_url_is_required(self):
    #     self.mock_Popen.return_value.returncode = 2
    #     wrapper = VerifyWrapper()

    #     result, output = wrapper.call_verify(provider_base_url='test')

    #     self.assertEqual(result, 2)

    #     # self.assertFalse(result)
    #     args, _ = self.mock_Popen.call_args

    #     self.assertIn('--provider-base-url=test', args[0])
    #     self.assertTrue(self.mock_Popen.called)
