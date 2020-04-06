import json
import requests
from api.urls import URLS
from data.auth import AUTH


class WrongAuthData(Exception):
    pass


class Client:
    def __init__(self, user=None, password=None):
        self.user = AUTH.get('email')
        self.password = AUTH.get('password')
        if user:
            self.user = user
        if password:
            self.password = password
        self.base_url = 'https://target.my.com/'
        self.session = requests.Session()
        self.csrf_token = None

    def _request(self, method, location, headers=None, params=None, data=None, redirect=False):
        return self.session.request(method, location, headers=headers, params=params, data=data, allow_redirects=redirect)

    def login(self):
        location = URLS.get('login_url')
        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email'
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'Referer': 'https://target.my.com/'
        }
        resp = self._request('POST', location, data=data, headers=headers)
        if URLS.get('error_url') in resp.headers['Location']:
            raise WrongAuthData
        for i in range(0, 4):  # Have to go throw 4 redirects to login
            location = resp.headers['Location']
            resp = self._request('GET', location)
        # Now we have to save csrf token to continue session
        location = URLS.get('csrf_url')
        resp = self._request('GET', location)
        self.csrf_token = resp.cookies['csrftoken']
        return resp.status_code

    def create_segment(self, data):
        location = URLS.get('create_url')
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'X-CSRFToken': self.csrf_token,
            'X-Requested-With': 'XMLHttpRequest'
        }
        return self._request('POST', location, headers=headers, data=data)

    def delete_segment(self, segment_id):
        location = URLS.get('delete_url') + f'{segment_id}.json'
        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.csrf_token
        }
        return self._request("DELETE", location, headers=headers)
