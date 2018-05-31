import json
import os
import sys
import socket
import unittest
from datetime import datetime
from ustutor.service import redis_store


def free_port_no(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def test_url(path, host='localhost', port=5000):
    return 'http://' + host + ':' + str(port) + path


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'app'):
            upper_path = os.path.abspath('.')
            sys.path.append(upper_path)
            from ustutor import create_app
            from ustutor import config
            self.port = free_port_no('localhost')
            app = create_app(config)
            self.client = app.test_client()
            self.app = app
            self.config = app.config
            self.app_context = self.app.app_context()
            self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        pass

    def register(self, username, user_type):
        redis_store.set("VC:" + username, "000000")
        r = self.client.post('/auth/register', data=json.dumps({
            "username": username, "password": username,
            "usertype": user_type, "verify_code": "000000"
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))
        return r

    def login(self, username, user_type):
        r = self.client.post('/auth/login', data=json.dumps({
            "username": username, "password": username,
            "usertype": user_type
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))
        return r


if __name__ == '__main__':
    unittest.main()