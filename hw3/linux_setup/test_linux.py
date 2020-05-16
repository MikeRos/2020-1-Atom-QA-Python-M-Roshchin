import pytest
import requests as rq
from requests import exceptions


PASSWORD = "centos"
NGINX_ADDR = "http://192.168.1.14:88"


def test_root(remote):
    ans = remote.exec_root("whoami")
    assert ans == 'root\n'


def test_nginx_ssh(remote):
    reply = remote.exec_root("netstat -tulpan | grep 88 | awk ' {print $4, $6} '")
    assert "88" in reply and "LISTEN" in reply


def test_nginx_http(remote):
    resp = rq.get(NGINX_ADDR)
    assert resp.status_code == 200


def test_nginx_access(remote):
    count_before = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print NR} '")
    rq.get(NGINX_ADDR)
    count_after = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print NR} '")
    last_l = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print} '")
    assert count_before < count_after and "python-requests" in last_l


def test_firewalld(remote):
    remote.exec_root("firewall-cmd --permanent --remove-port=88/tcp")
    remote.exec_root("firewall-cmd --reload")
    nginx_state = remote.exec_root("systemctl status nginx")
    with pytest.raises(exceptions.ConnectionError):
        assert rq.get(NGINX_ADDR) and "active (running)" in nginx_state
    # Add port back again for next tests
    remote.exec_root("firewall-cmd --permanent --add-port=88/tcp")
    remote.exec_root("firewall-cmd --reload")
