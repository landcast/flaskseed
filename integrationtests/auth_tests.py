import json
import subprocess
import os
import sys
import unittest
sys.path.append('.')
from integrationtests import random_username, redis_store, TestBase

json_header = '"Content-Type:application/json"'

server_location = 'http://t.vipustutor.com:5000'


class AuthTest(TestBase):

    def test_register(self):
        username = random_username()
        verify_code = "000000"
        redis_store.set("VC:" + username, verify_code)
        register_url = f'{server_location}/auth/register'
        json_data = "'" + json.dumps({
            "username": username,
            "usertype": "SysUser",
            "password": "123456",
            "verify_code": "123456"
        }) + "'"
        cmd = f'''
            curl -i -H {json_header} -X POST --data {json_data} {register_url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        self.logger.debug(output)


if __name__ == "__main__":
    unittest.main()