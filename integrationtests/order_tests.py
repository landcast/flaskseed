import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta
sys.path.append('.')
from integrationtests import random_username, TestBase, redis_store, logger


json_header = '"Content-Type:application/json"'

server_location = 'http://127.0.0.1:5000'


class OrderCurlTest(TestBase):

    def test_register(self):
        url = f'{server_location}/order/main_query'
        end = (datetime.now() + timedelta(seconds=30)).isoformat()[:-3] + 'Z'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "created_at_start": start,
            "created_at_end": end
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
