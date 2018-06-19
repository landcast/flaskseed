import json
import subprocess
import sys
import unittest
sys.path.append('.')
from integrationtests import random_username, TestBase, redis_store, logger


json_header = '"Content-Type:application/json"'

server_location = 'http://127.0.0.1:5000'


class OrderCurlTest(TestBase):

    def test_register(self):
        url = f'{server_location}/order/main_query'
        json_data = "'" + json.dumps({
            "page_no": 0,
            "page_limit": 10,
            "start": "2018-06-18 23:00:00.000",
            "end": "2018-06-19 23:00:00.000"
        }) + "'"
        cmd = f'''
            curl -sS -i -H {json_header} -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')


if __name__ == "__main__":
    unittest.main()
