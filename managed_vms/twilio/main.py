# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import os

from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient


# [START configuration]
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
# [END configuration]


app = Flask(__name__)


# [START receive_call]
@app.route('/call/receive', methods=['POST'])
def receive_call():
    """Answers a call and replies with a simple greeting."""
    response = twiml.Response()
    response.say('Hello from Twilio!')
    return str(response), 200, {'Content-Type': 'application/xml'}
# [END receive_call]


# [START send_sms]
@app.route('/sms/send')
def send_sms():
    """Sends a simple SMS message."""
    to = request.args.get('to')
    if not to:
        return ('Please provide the number to message in the "to" query string'
                ' parameter.')

    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    rv = client.messages.create(
        to=to,
        from_=TWILIO_NUMBER,
        body='Hello from Twilio!')
    return str(rv)
# [END send_sms]


# [START receive_sms]
@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    """Receives an SMS message and replies with a simple greeting."""
    sender = request.values.get('From')
    body = request.values.get('Body')

    message = 'Hello, {}, you said: {}'.format(sender, body)

    response = twiml.Response()
    response.message(message)
    return str(response), 200, {'Content-Type': 'application/xml'}
# [END receive_sms]


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See CMD in Dockerfile.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
