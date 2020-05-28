import threading
import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)
users = {'ADMIN_USER': 'vk_6897345'}
host = '127.0.0.1'
port = 5000


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    func = request.environ.get('werkzeug.test_server.shutdown')
    if func:
        func()
    else:
        raise RuntimeError('Not running with the Werkzeug Server')


# TODO use data from tests
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    vk_id = request.form['vk_id']
    users.update({username: vk_id})


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username: str):
    # check if we added this user earlier first
    if username in users:
        vk_id = users[username]
        resp = {'vk_id': vk_id}
        return jsonify(resp)
    else:
        return jsonify({}), 404
        # vk_id = {}
        # # some magic to simulate missing users
        # if is_hash_ok(username):
        #     # Trying to return something that looks like id
        #     vk_id = 'vk_' + str(int.from_bytes(username.encode(), 'little') % 10000000)
        #     resp = {'vk_id': vk_id}
        #     return jsonify(resp)
        # else:
        #     return jsonify(vk_id), 404


@app.route('/name_with_valid_id', methods=['GET'])
def get_name_with_vk_id():
    # some magic to simulate valid users
    name_length = random.randint(3, 8)
    name = ''
    for i in range(3):  # 3 tries to get valid name, else return 404
        for k in range(name_length):
            name += random.choice(string.ascii_letters)
        if is_hash_ok(name):
            break
        else:
            name = ''
    if name != '':
        return jsonify({'valid_name': name})
    else:
        return jsonify({}), 404


@app.route('/shutdown')
def shutdown():
    shutdown_mock()


if __name__ == '__main__':
    run_mock()


def is_hash_ok(name):
    my_little_hash = 0
    for s in name:
        my_little_hash += ord(s)
    if my_little_hash % 10 > 7:
        return None
    return my_little_hash
