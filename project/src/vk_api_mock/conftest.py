import pytest
import requests
import time
from src.vk_api_mock.app import run_mock


@pytest.fixture(scope='session')
def mock_server():
    server = run_mock()
    server_host = server._kwargs['host']
    server_port = server._kwargs['port']
    time.sleep(1)
    yield server_host, server_port
    shutdown_url = f'http://{server_host}:{server_port}/shutdown'
    requests.get(shutdown_url)
