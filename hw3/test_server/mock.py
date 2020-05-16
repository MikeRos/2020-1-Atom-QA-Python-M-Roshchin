import threading
from flask import Flask, abort, request

app = Flask(__name__)
users = dict()
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


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = users.get(int(user_id), None)
    if user:
        return user
    else:
        abort(404)


@app.route('/add_user', methods=['POST'])
def add_user():
    next_user_id = len(users)
    data = {"name": request.form['username'], "surname": request.form['surname']}
    users.update({next_user_id: data})


@app.route('/shutdown')
def shutdown():
    shutdown_mock()


if __name__ == '__main__':
    run_mock()
