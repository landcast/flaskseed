import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta
sys.path.append('.')
from integrationtests import random_username, TestBase, redis_store, logger


json_header = '"Content-Type:application/json"'

server_location = 'http://127.0.0.1:5000'


class StudentTest(TestBase):

    def test_my_course(self):
        url = f'{server_location}/student/my_course'
        end = (datetime.now() + timedelta(seconds=30)).isoformat()[:-3] + 'Z'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "course_time": start
        }) + "'"
        cmd = f'''
            curl -sS -i -H {json_header} -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')

    def test_my_order(self):
        url = f'{server_location}/student/my_order'
        end = (datetime.now() + timedelta(seconds=30)).isoformat()[:-3] + 'Z'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "course_time": start,
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
