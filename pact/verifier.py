"""Classes and methods to verify Contracts."""

class Verifier(object):
    """A Pact Verifier."""

    def __init__(self, **kwargs):
        """Create a new Verifier.

        :param kwargs: The name of this provider. This will be shown in the Pact
            when it is published.
        """
        self.provider = kwargs['provider']
        print(self.provider)

    def __str__(self):
        """Return string representation.

        Returns:
            [String]: verifier description.

        """
        return 'Verifier for {}'.format(self.provider)

    def verify(self, **kwargs):
        """Verify our pacts from the provider.

        Returns:
          [provider]: [tbd]

        """
        print('verify')
        return self.provider
