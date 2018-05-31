#!/usr/bin/env python
# from mockito import mock, verify
import json
import unittest
import os
import sys
import subprocess
from datetime import datetime

sys.path.append(".")
from unittests.test_base import TestBase, random_username
from ustutor.service.emailservice import create_email_attachment, send_email


class EmailServiceTest(TestBase):
    auth_header = None
    student_id = 0
    token = None
    channel_name = None
    channel_id = 0
    enrollment_id = 0

    def setUp(self):
        super().setUp()
        test_user = random_username()
        self.auth_header = json.loads(
            super().register(test_user, 'Student').get_data(as_text=True))
        self.token = self.auth_header[self.config['JWT_HEADER']]
        self.app.logger.debug("jwt:" + self.token)
        os.system("echo '中文内容' | cat > ./中文文件.txt")

    def tearDown(self):
        r1 = subprocess.run(['rm', './中文文件.txt'], subprocess.PIPE)
        self.app.logger.debug(r1.stdout)

    def test_send_attachment(self):
        att = create_email_attachment('中文文件.txt')
        # print(type(att))
        send_email(['landcast@163.com'], subject='test for attachement',
                   body='none', attachments=[att])


if __name__ == '__main__':
    unittest.main()
