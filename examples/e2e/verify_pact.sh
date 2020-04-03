#!/bin/bash
set -o pipefail

python provider.py & &>/dev/null
FLASK_PID=$!

echo $FLASK_PID

quit() {
    # some weirdness about where this process is running so have to get the child
    echo "Kill $1"
    CHILD=`pgrep -P $1`

    kill -9 $CHILD
    exit $?
}

VERSION=$1
if [ -x $VERSION ]; then
    echo "ERROR: You must specify a provider version"
    exit
fi

pact-verifier --provider-base-url=http://localhost:5001 \
  --provider-app-version $VERSION \
  --provider-states-setup-url=http://localhost:5001/_pact/provider_states \
  tests/userserviceclient-userservice.json


quit $FLASK_PID

# quit
  #   --pact-url="http://127.0.0.1/pacts/provider/UserService/consumer/UserServiceClient/latest" \
  # --provider-states-setup-url=http://localhost:5001/_pact/provider_states \
  #  --pact-broker-username pactbroker \
  # --pact-broker-password pactbroker \
  # --publish-verification-results \
