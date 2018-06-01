import logging
import os
import redis
import subprocess
import time
import unittest

from config import settings
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
redis_store = redis.from_url(settings.REDIS_URL)


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittest.TestCase):

    def server_check(self):
        pid_file_path = "./" + settings.PID_FILE + ".pid"
        if os.path.exists(pid_file_path):
            logger.debug('step 10')
            with open(pid_file_path, 'r+') as pidfile:
                logger.debug('step 11')
                old_pid = pidfile.read()
                # check process exist or not
                output = subprocess.getoutput('ps -q ' + old_pid)
                if old_pid not in output:
                    logger.debug('step 12')
                    logger.debug('start new server')
                    os.system(
                        'nohup python run.py > /dev/null 2>&1 &')
                    time.sleep(2)
                    logger.debug('step 13')
        else:
            logger.debug('step 20')
            logger.debug(os.getcwd())
            os.system('nohup python run.py > /dev/null 2>&1 &')
            time.sleep(2)
            logger.debug('step 21')

    def setUp(self):
        self.server_check()

    def tearDown(self):
        pass
