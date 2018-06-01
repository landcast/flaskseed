import logging
import os
import redis
import subprocess
import time
import unittest

from config import settings
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
redis_store = redis.from_url(settings.REDIS_URL)


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittest.TestCase):

    def server_check(self):
        pid_file_path = settings.PID_FILE + ".pid"
        if os.path.exists(pid_file_path):
            with open(pid_file_path, 'r+') as pidfile:
                old_pid = pidfile.read()
                # check process exist or not
                output = subprocess.getoutput('ps -q ' + old_pid)
                if old_pid not in output:
                    logger.debug('start new server')
                    os.system(
                        'nohup python run.py > /dev/null 2>&1 &')
                    time.sleep(2)
        else:
            os.system('nohup python run.py > /dev/null 2>&1 &')
            time.sleep(2)

    def setUp(self):
        self.server_check()

    def tearDown(self):
        pass
