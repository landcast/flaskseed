import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta
sys.path.append('.')
from integrationtests import TestBase, json_header, server_location


class OrderCurlTest(TestBase):
    '''

    '''
    def test_register(self):
        url = f'{server_location}/order/main_query'
        end = (datetime.now() + timedelta(seconds=30)).isoformat()[:-3] + 'Z'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "order_type": "1",
            "created_at_start": start,
            "created_at_end": end
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "order_type": "2"
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')


if __name__ == "__main__":
    unittest.main()
