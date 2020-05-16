import pytest
from test_server.client import Client
import json


class TestFlask:

    def test_default_user(self, mock_server):
        server_host, server_port = mock_server
        url = f'http://{server_host}:{server_port}/user/0'
        client = Client(target_host=server_host, target_port=server_port)
        client.get_request(url)
        resp = json.loads(client.get_resp())
        body = json.loads(resp['body'])
        assert body['surname'] == 'User'

    def test_invalid(self, mock_server):
        server_host, server_port = mock_server
        url = f'http://{server_host}:{server_port}/user/999'
        client = Client(target_host=server_host, target_port=server_port)
        client.get_request(url)
        resp = json.loads(client.get_resp())
        assert resp['resp_code'] == '404'
