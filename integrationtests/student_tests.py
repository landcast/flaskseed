import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta

sys.path.append('.')
from integrationtests import random_username, TestBase, json_header, \
    server_location
from config.settings import JWT_HEADER


class StudentTest(TestBase):

    def test_my_course(self):
        output = self.json_register(random_username(), 'Student')
        header = JWT_HEADER + ":" + output[JWT_HEADER]
        url = f'{server_location}/student/my_course'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1,
            "course_time": start
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -H '{header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')

    def test_my_order(self):
        output = self.json_register(random_username(), 'Student')
        header = JWT_HEADER + ":" + output[JWT_HEADER]
        url = f'{server_location}/student/my_order'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -H '{header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')

    def test_my_homework(self):
        output = self.json_register(random_username(), 'Student')
        header = JWT_HEADER + ":" + output[JWT_HEADER]
        url = f'{server_location}/student/my_homework'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        json_data = "'" + json.dumps({
            "page_no": 1,
            "page_limit": 1
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -H '{header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')


if __name__ == "__main__":
    unittest.main()
