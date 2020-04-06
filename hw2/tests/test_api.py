import pytest
from api.client import WrongAuthData, Client


@pytest.mark.API
class TestApi:
    def test_auth(self):
        client = Client()
        assert client.login() == 200

    def test_fail_auth(self):
        wrong_data = ('test@testmail.tst', 'password42')
        client = Client(wrong_data)
        with pytest.raises(WrongAuthData):
            client.login()

    def test_create_segment(self, test_segment_data):
        client = Client()
        client.login()
        response = client.create_segment(test_segment_data)
        assert response.status_code == 200

    def test_delete_segment(self, test_segment_data):
        client = Client()
        client.login()
        response = client.create_segment(test_segment_data)
        segment_id = response.json()['id']
        response = client.delete_segment(segment_id)
        assert response.status_code == 204
