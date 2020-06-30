"""Classes and methods to verify Contracts."""
from pact.verify_wrapper import VerifyWrapper

class Verifier(object):
    """A Pact Verifier."""

    def __init__(self, **kwargs):
        """Create a new Verifier.

        :param kwargs: The name of this provider. This will be shown in the Pact
            when it is published.
        """
        self.provider = kwargs['provider']
        self.provider_base_url = kwargs['provider_base_url']

    def __str__(self):
        """Return string representation.

        Returns:
            [String]: verifier description.

        """
        return 'Verifier for {}'.format(self.provider)

    def verify_pacts(self, *pacts, **kwargs):
        """Verify our pacts from the provider.

        Returns:
          [provider]: [tbd]

        """
        success, logs = VerifyWrapper().call_verify(*pacts,
                                                    provider=self.provider,
                                                    provider_base_url=self.provider_base_url)
        return success, logs

    def verify_with_broker(self, broker_username, broker_password, broker_url):
        """Use Broker to verify.

        Args:
            broker_username ([String]): broker username
            broker_password ([String]): broker password
            broker_url ([String]): url of broker

        """
        success, logs = VerifyWrapper().call_verify(broker_username=broker_username,
                                                    broker_password=broker_password,
                                                    broker_url=broker_url,
                                                    provider=self.provider,
                                                    provider_base_url=self.provider_base_url)
        return success, logs
