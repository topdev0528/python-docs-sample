# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64

import copy

from uuid import uuid4

import pytest

import main


required_fields = ['Ce-Id', 'Ce-Source', 'Ce-Type', 'Ce-Specversion']

header_data = {field: str(uuid4()) for field in required_fields}


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_empty_payload(client):
    r = client.post('/', json='', headers=header_data)
    assert r.status_code == 400


def test_invalid_payload(client):
    r = client.post('/', json={'nomessage': 'invalid'}, headers=header_data)
    assert r.status_code == 400


def test_invalid_mimetype(client):
    r = client.post('/', json="{ message: true }", headers=header_data)
    assert r.status_code == 400


def test_minimally_valid_message(client, capsys):
    r = client.post('/', json={'message': True}, headers=header_data)
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    ce_id = header_data['Ce-Id']
    assert f'Hello, World! ID: {ce_id}' in out


def test_populated_message(client, capsys):
    name = str(uuid4())
    data = base64.b64encode(name.encode()).decode()

    r = client.post('/', json={'message': {'data': data}}, headers=header_data)
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    ce_id = header_data['Ce-Id']
    assert f'Hello, {name}! ID: {ce_id}' in out


def test_missing_required_fields(client, capsys):
    for field in required_fields:
        test_headers = copy.copy(header_data)
        test_headers.pop(field)

        r = client.post('/', headers=test_headers)
        assert r.status_code == 400

        out, _ = capsys.readouterr()
        assert f'Bad Request: missing required header {field}' in out
