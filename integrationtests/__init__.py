import logging
import os
import sys
import redis
import subprocess
import time

from config import settings
from datetime import datetime
import unittests.test_base
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
redis_store = redis.from_url(settings.REDIS_URL)


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittests.test_base.TestBase):

    json_header = 'Content-Type:application/json'
    server_location = 'http://127.0.0.1:5000'

    def register(self, username, user_type):
        verify_code = "000000"
        redis_store.set("VC:" + username, verify_code)
        register_url = f'{self.server_location}/auth/register'
        json_data = "'" + json.dumps({
            "username": username,
            "usertype": user_type,
            "password": "123456",
            "verify_code": "000000"
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{self.json_header}' -X POST --data {json_data} {
            register_url}
            '''
        status_code, output = subprocess.getstatusoutput(cmd)
        return status_code, output

    def json_register(self, username, user_type):
        status_code, output = self.register(username, user_type)
        json_str = re.findall(r"\{(.*)\}", output, re.S)
        return json.loads('{' + json_str[0].replace('\n', '') + '}')

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
                    logger.debug('start new server ' + str(datetime.now()))
                    subprocess.Popen(
                            'python run.py',
                            shell=True, start_new_session=True)
                    time.sleep(2)
                    logger.debug('step 13 ' + str(datetime.now()))
        else:
            logger.debug('step 20 ' + str(datetime.now()))
            logger.debug(os.getcwd())
            subprocess.Popen(
                    'python run.py ',
                    shell=True, start_new_session=True)
            time.sleep(2)
            logger.debug('step 21 ' + str(datetime.now()))

    def setUp(self):
        self.server_check()

    def tearDown(self):
        pass
