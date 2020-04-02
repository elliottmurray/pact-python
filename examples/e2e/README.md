# Introduction

This is an e2e example using flask to help as a guide to getting started with Pact for Python

## Setup

Create your own virtualenv for this. Run

```bash
pip install -r requirements.txt
```

## Consumer

From the root directory run:

```bash
pytest
```

Or you can run individual tests like:

```bash
pytest tests/test_user_consumer.py::test_get_non_existing_user
```

Sometimes you may get the mock server in a hung state. You can kill it via (untested):

```bash
pkill -f pact-mock-service.rb
```

## Provider States

To manually trigger one of the 2 manual states you can run:

```bash
curl -X POST -H "Content-Type: application/json"  --data "{\"state\": \"UserA exists and is not an administrator\"}" http://127.0.0.1:5000/_pact/provider_states
```

Changing the json content to match the state you want.
