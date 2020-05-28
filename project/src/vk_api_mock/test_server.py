from src.vk_api_mock.client import Client


class TestFlask:

    def test_default_user(self, mock_server):
        server_host, server_port = mock_server
        test_name = "Test_Name"
        print(test_name)
        url = f'http://{server_host}:{server_port}/vk_id/{test_name}'
        client = Client(target_host=server_host, target_port=server_port)
        client.get_request(url)
        resp = client.get_resp()
        print()
        print(resp)
        assert resp
