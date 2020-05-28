import json
import requests
from data.urls import *


class Response:
    def __init__(self, req_resp):
        self.status = req_resp.status_code
        self.headers = req_resp.headers
        self.cookies = req_resp.cookies
        try:
            self.content_type = req_resp.headers['Content-Type']
        except KeyError:
            pass
        try:
            self.body = req_resp.json()
        except ValueError:
            self.body = req_resp.content

    def __repr__(self):
        return f'Status: {self.status}\n' \
               f'Content-type: {self.content_type}\n' \
               f'Headers: {self.headers}\n' \
               f'Body: {self.body}\n'


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session_cookie = None
        self.vary = None

    def _request(self, method, url, headers=None, params=None, data=None, redirect=False):
        return self.session.request(method, url=url, headers=headers, params=params, data=data,
                                    allow_redirects=redirect, verify=False)

    def get_req(self, url):
        return Response(self._request('GET', url))

    def login(self, username, password):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Refer": "http://localhost:8080/login"
        }
        payload = 'username=' + username + '&password=' + password + '&submit=Login'
        Response(self._request('POST', url=URL_LOGIN, data=payload, headers=headers))

    def check_status(self):
        return Response(self._request('GET', URL_STATUS))

    def add_user(self, username, password, email):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            'username': f"{username}",
            'password': f"{password}",
            'email': f"{email}"
        }
        return Response(self._request('POST', url=ADD_USER, data=json.dumps(payload), headers=headers))

    def bad_request(self, username, password, email):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            'username': f"{username}",
            'password': f"{password}",
            'email': f"{email}"
        }
        return Response(self._request('POST', url=ADD_USER, data=payload, headers=headers))

    def del_user(self, username):
        url = DEL_USER + username
        return Response(self._request('GET', url))

    def block_user(self, username):
        url = BLOCK_USER + username
        return Response(self._request('GET', url))

    def accept_user(self, username):
        url = ACCEPT_USER + username
        return Response(self._request('GET', url))
