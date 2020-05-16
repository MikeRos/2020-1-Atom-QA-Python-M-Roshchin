import socket
import time
import json


class Client:
    def __init__(self, target_host, target_port):
        self.s = socket.socket()
        self.port = target_port
        self.host = target_host

    def get_resp(self):
        time.sleep(0.1)
        recv = self.s.recv(4096).decode('utf-8')
        recv = recv.split('\r\n\r\n')
        headers = recv[0].split('\r\n')
        start_line = headers.pop(0)
        headers_dict = {}
        for header in headers:
            print(header)
            pair = header.split(': ')
            headers_dict[pair[0]] = pair[1]
        body = recv[1].rstrip('\n')
        response = {'start_line': start_line, 'resp_code': start_line.split(' ')[1], 'headers': headers_dict,
                    'body': body}
        res = json.dumps(response)
        print(res)
        return res

    def get_request(self, endpoint):
        self.s.connect((self.host, self.port))
        request = f'GET {endpoint} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.s.send(request.encode())

    def post_request(self, endpoint, username, surname):
        self.s.connect((self.host, self.port))
        body = f'username={username}&surname={surname}'
        headers = (f'POST {endpoint} HTTP/1.1\r\n'
                   f'Content-Type: application/x-www-form-urlencoded\r\n'
                   f'Content-Length: {len(body)}\r\n'
                   f'Host: {self.host}:{self.port}\r\n'
                   f'Connection: close\r\n\r\n')
        payload = headers + body
        self.s.send(payload.encode())
