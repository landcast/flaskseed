import json
import os
import sys
import socket
import unittest
from datetime import datetime
from src.service import redis_store


def free_port_no(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'app'):
            upper_path = os.path.abspath('.')
            sys.path.append(upper_path)
            from src import create_app
            from config import settings
            self.port = free_port_no('localhost')
            app = create_app(settings)
            self.client = app.test_client()
            self.app = app
            self.config = app.config
            self.logger = app.logger
            self.app_context = self.app.app_context()
            self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        pass