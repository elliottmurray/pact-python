# Title

This was taken from https://github.com/bsquizz/pact-python-demo/blob/master/pact_python_demo/user-app.py
and modified.

## Setup

Run
```bash
pip install -r requirements.txt
```


## Provider States

To manually trigger one of the 2 manual states you can run:

```bash
curl -X POST -H "Content-Type: application/json"  --data "{\"state\": \"UserA exists and is not an administrator\"}" http://127.0.0.1:5000/_pact/provider_states
```

Changing the json content to match the state you want.
