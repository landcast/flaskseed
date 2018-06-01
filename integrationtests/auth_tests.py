import json
import subprocess
import sys
import unittest
sys.path.append('.')
from integrationtests import random_username, TestBase, redis_store, logger


json_header = '"Content-Type:application/json"'

server_location = 'http://127.0.0.1:5000'


class CurlTest(TestBase):

    def test_register(self):
        username = random_username()
        verify_code = "000000"
        redis_store.set("VC:" + username, verify_code)
        register_url = f'{server_location}/auth/register'
        json_data = "'" + json.dumps({
            "username": username,
            "usertype": "SysUser",
            "password": "123456",
            "verify_code": "000000"
        }) + "'"
        cmd = f'''
            curl -sS -i -H {json_header} -X POST --data {json_data} {
            register_url}
            '''
        logger.debug(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        logger.debug(output)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')


if __name__ == "__main__":
    unittest.main()
