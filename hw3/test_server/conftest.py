import pytest
import requests
from test_server.mock import run_mock
import time
from test_server.client import Client


@pytest.fixture(scope='session')
def mock_server():
    server = run_mock()
    server_host = server._kwargs['host']
    server_port = server._kwargs['port']
    time.sleep(1)
    client = Client(target_host=server_host, target_port=server_port)
    client.post_request('/add_user', 'First', 'User')

    yield server_host, server_port

    shutdown_url = f'http://{server_host}:{server_port}/shutdown'
    requests.get(shutdown_url)
