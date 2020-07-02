"""Wrapper to verify previously created pacts."""

from pact.constants import VERIFIER_PATH
import sys
import os
import platform

import subprocess
from os.path import isdir, join, isfile
from os import listdir

def capture_logs(process, verbose):
    """Capture logs from ruby process."""
    result = ''
    for line in process.stdout:
        result = result + line + '\n'

    return result


def path_exists(path):
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

def sanitize_logs(self, process, verbose):
    """
    Print the logs from a process while removing Ruby stack traces.

    :param process: The Ruby pact verifier process.
    :type process: subprocess.Popen
    :param verbose: Flag to toggle more verbose logging.
    :type verbose: bool
    :rtype: None
    """
    for line in process.stdout:
        if (not verbose and line.lstrip().startswith('#')
                and ('vendor/ruby' in line or 'pact-provider-verifier.rb' in line)):
            continue
        else:
            sys.stdout.write(line)


class PactException(Exception):
    """PactException when input isn't valid.

    Args:
        Exception ([type]): [description]

    Raises:
        KeyError: [description]
        Exception: [description]

    Returns:
        [type]: [description]

    """

    def __init__(self, *args, **kwargs):
        """Create wrapper."""
        super().__init__(*args, **kwargs)
        self.message = args[0]

class VerifyWrapper(object):
    """A Pact Verifier Wrapper."""

    def _broker_present(self, **kwargs):
        if (kwargs.get('broker_username') is None
            or kwargs.get('broker_password') is None
                or kwargs.get('broker_url') is None):

            return False

        return True

    def call_verify(self, *pacts, provider_base_url, provider, **kwargs):
        """Call verify method."""
        print(pacts)
        print(kwargs)
        print(provider_base_url)

        if not pacts and not self._broker_present(**kwargs):
            raise PactException('Pact urls or Pact broker required')

        options = {
            '--provider-base-url': provider_base_url,
            '--provider': provider,
            '--broker-username': kwargs.get('broker_username', None),
            '--broker-password': kwargs.get('broker_password', None),
            '--pact-broker-base-url': kwargs.get('broker_url', None)

            # '--provider-states-setup-url': states_setup_url,
            # '--broker-token': token,
            # '--log-dir': log_dir,
            # '--log-level': log_level
        }

        command = [VERIFIER_PATH]
        all_pact_urls = self.expand_directories(list(pacts))

        command.extend(all_pact_urls)
        command.extend(['{}={}'.format(k, v) for k, v in options.items() if v])

        verbose = "undefined"
        env = os.environ.copy()
        env['PACT_INTERACTION_RERUN_COMMAND'] = self.rerun_command()
        result = subprocess.Popen(command, bufsize=1, env=env, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, universal_newlines=True)

        # self.sanitize_logs(result, verbose)
        logs = capture_logs(result, verbose)

        result.wait()
        return result.returncode, logs

    def expand_directories(self, paths):
        """
        Iterate over paths and expand any that are directories into file paths.

        :param paths: A list of file paths to expand.
        :type paths: list
        :return: A list of file paths with any directory paths replaced with the
            JSON files in those directories.
        :rtype: list
        """
        paths_ = []
        for path in paths:
            if path.startswith('http://') or path.startswith('https://'):
                paths_.append(path)
            elif isdir(path):
                paths_.extend(
                    [join(path, p) for p in listdir(path) if p.endswith('.json')])
            else:
                paths_.append(path)

        # Ruby pact verifier expects forward slashes regardless of OS
        return [p.replace('\\', '/') for p in paths_]

    def rerun_command(self):
        """
        Create a rerun command template for failed interactions.

        :rtype: str
        """
        is_windows = 'windows' in platform.platform().lower()
        if is_windows:
            return (
                'cmd.exe /v /c "'
                'set PACT_DESCRIPTION=<PACT_DESCRIPTION>'
                '& set PACT_PROVIDER_STATE=<PACT_PROVIDER_STATE>'
                '& {command}'
                ' & set PACT_DESCRIPTION='
                ' & set PACT_PROVIDER_STATE="'.format(command=' '.join(sys.argv)))
        else:
            return ("PACT_DESCRIPTION='<PACT_DESCRIPTION>'"
                    " PACT_PROVIDER_STATE='<PACT_PROVIDER_STATE>'"
                    " {command}".format(command=' '.join(sys.argv)))
