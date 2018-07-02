import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta

sys.path.append('.')
from integrationtests import TestBase, json_header, server_location


class CourseTest(TestBase):

    def test_course(self):
        url = f'{server_location}/test/add_account_single_session'
        json_data = "'" + json.dumps({
            "state": 1,
            "account_name": 'litao',
            "account_no": "0123456789"
        }) + "'"
        cmd = f'''
            curl -sS -i -H '{json_header}' -X POST --data {json_data} {url}
            '''
        print(cmd)
        status_code, output = subprocess.getstatusoutput(cmd)
        print(output)
        self.assertTrue('200 OK' in output, 'expect http status return 200')

        url = f'{server_location}/test/add_account_nested_session'
        json_data = "'" + json.dumps({
            "state": 1,
            "account_name": 'tom',
            "account_no": "1111111111"
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