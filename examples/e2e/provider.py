import datetime
import json
import uuid

from flask import Flask, abort, jsonify, request

fakedb = {}

app = Flask(__name__)


@app.route('/_pact/provider_states', methods=['POST'])
def provider_states():
    mapping = {'UserA does not exist': setup_no_user_a,
               'UserA exists and is not an administrator': setup_user_a_nonadmin}
    mapping[request.json['state']]()
    return jsonify({'result': request.json['state']})


def setup_no_user_a():
    if 'UserA' in fakedb:
        del fakedb['UserA']


def setup_user_a_nonadmin():
    broken_id = '1234567'
    working_id = '00000000-0000-4000-a000-000000000000'
    broken_date = datetime.datetime.now()
    working_date = '2016-12-15T20:16:01'

    fakedb['UserA'] = {
                        'name': "UserA",
                        'id': broken_id,
                        'created_on': broken_date,
                        'admin': False
                      }


@app.route('/users/<name>')
def get_user_by_name(name):
    user_data = fakedb.get(name)
    if not user_data:
        abort(404)
    response = jsonify(**user_data)
    app.logger.debug('get user for %s returns data:\n%s', name, response.data)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5001)
