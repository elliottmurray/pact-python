"""Classes and methods to verify Contracts."""
from os.path import isfile

from pact.verify_wrapper import VerifyWrapper

class Verifier(object):
    """A Pact Verifier."""

    def __init__(self, provider, provider_base_url, **kwargs):
        """Create a new Verifier.

        Args:
            provider ([String]): provider name
            provider_base_url ([String]): provider url

        """
        self.provider = provider
        self.provider_base_url = provider_base_url

    def __str__(self):
        """Return string representation.

        Returns:
            [String]: verifier description.

        """
        return 'Verifier for {} with url {}'.format(self.provider, self.provider_base_url)

    def verify_pacts(self, *pacts, **kwargs):
        """Verify our pacts from the provider.

        Returns:
          success: True if no failures
          logs: some tbd output of logs

        """
        missing_files = [path for path in pacts if not self.path_exists(path)]
        print("!!!!!!")
        if missing_files:
            raise Exception("Missing pact files {}".format(missing_files))

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

    def path_exists(self, path):
        """
        Determine if a particular path exists.

        Can be provided a URL or local path. URLs always result in a True. Local
        paths are True only if a file exists at that location.

        :param path: The path to check.
        :type path: str
        :return: True if the path exists and is a file, otherwise False.
        :rtype: bool
        """
        if path.startswith('http://') or path.startswith('https://'):
            return True

        print(path)
        print(isfile(path))
        return isfile(path)
