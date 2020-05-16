import pytest
from linux_setup.ssh_client import SSH


@pytest.fixture(scope='session')
def remote():
    with SSH(hostname='192.168.1.14', username='centos', password='centos', port=2222) as ssh:
        yield ssh
