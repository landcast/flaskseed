#!/usr/bin/env python
from datetime import datetime
# from mockito import mock, verify
import json
import random
import requests
import unittest
import sys

sys.path.append(".")
from unittests.test_base import TestBase, random_username


class SmsTest(TestBase):

    def test_smsverifycode(self):
        """
        Integer type; //类型（1：注册时调用 2：重置密码时调用）
        String userName;//手机号/邮件
        Integer registerType; //验证码类型， 1：手机号注册 2：邮箱注册
        String countryCode; // 国家电话代码
        String code //随机码
        :return:
        """
        r = requests.post(
            self.config['EP_LOCATION'] + self.config['EP_SMS_PATH'],
            data=json.dumps({
                'type': 1,
                'userName': '13521273258',
                'registerType': 1,
                'countryCode': '86',
                'code': str(random.randint(100000, 999999))
            }), headers={'Content-type': 'application/json'})
        self.assertEqual(0, r.json()['code'], 'returned code not 0')
        self.app.logger.debug(r.status_code)
        self.app.logger.debug(r.json()['message'])


if __name__ == "__main__":
    unittest.main()
