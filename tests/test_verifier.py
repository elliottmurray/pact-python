from unittest import TestCase
from mock import patch

from pact.verifier import Verifier
from pact.verify_wrapper import VerifyWrapper

PACT_FILE = 'test.pact'

class VerifierTestCase(TestCase):

    def setUp(self):
        super(VerifierTestCase, self).setUp()
        self.addCleanup(patch.stopall)

        # patch.object()
        self.mock_wrapper = patch.object(
            VerifyWrapper, 'call_verify', spec=True).start()

    def test_verifier_with_provider_and_urls(self):
        verifier = Verifier(provider='test_provider',
                            provider_base_url="http://localhost:8888")
        self.mock_wrapper.return_value = (True, 'some logs')

        output, _ = verifier.verify_pacts('path/to/pact1',
                                          'path/to/pact2')
        # provider='test',
        #                   broker_username=pact_broker_username,
        #                   pact_broker_password=pact_broker_password,
        #                   publish_verification_result=True,
        #                   provider_version=1.0,
        #                   pact_broker_url="http://locqlhost:1234")

        #   pacts, base_url, pact_url, pact_urls, states_url, states_setup_url,
        #  username, broker_base_url, consumer_version_tag, provider_version_tag,
        #  password, token, provider, headers, timeout, provider_app_version,
        #  publish_verification_results, verbose, log_dir, log_level

        self.assertTrue(output)
        self.assertEqual(self.mock_wrapper.call_count, 1)
        args, kwargs = self.mock_wrapper.call_args
        self.assertEquals('path/to/pact1', args[0])
        self.assertEquals('path/to/pact2', args[1])
        self.assertDictEqual({'provider': 'test_provider',
                              'provider_base_url': 'http://localhost:8888'},
                             kwargs)

    def test_verifier_with_broker(self):
        pact_broker_username = 'broker_username'
        pact_broker_password = 'broker_password'

        self.mock_wrapper.return_value = (True, 'ddf')

        verifier = Verifier(provider='test_provider',
                            provider_base_url="http://localhost:8888")

        output, _ = verifier.verify_with_broker(broker_username=pact_broker_username,
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
