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

import os

from flask import Flask
from pymemcache.client.base import Client as MemcacheClient


app = Flask(__name__)


# [START client]
memcache_addr = os.environ.get('MEMCACHE_PORT_11211_TCP_ADDR', 'localhost')
memcache_port = os.environ.get('MEMCACHE_PORT_11211_TCP_PORT', 11211)
memcache_client = MemcacheClient((memcache_addr, int(memcache_port)))
# [END client]


# [START example]
@app.route('/')
def index():

    # Set initial value if necessary
    if not memcache_client.get('counter'):
        memcache_client.set('counter', 0)

    value = memcache_client.incr('counter', 1)

    return 'Value is {}'.format(value)
# [END example]


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
