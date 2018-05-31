#!/usr/bin/env python
# from mockito import mock, verify
import unittest
import sys
import json

sys.path.append(".")
from unittests.test_base import TestBase, random_username
from ustutor.service.redisservice import redis_store


class AllAuthTest(TestBase):

    def register_login(self, username, user_type):
        status1 = super().register(username, user_type).status_code
        self.assertEqual(200,
                         status1,
                         "Failed! Random username register failed in test")

        status2 = super().login(username, user_type).status_code
        self.assertEqual(200, status2,
                         "Failed! Preset user can't login, login failed "
                         "in test")

        status3 = super().register(random_username(), user_type).status_code
        self.assertEqual(200, status3,
                         "Failed! Random username register failed in test")

        status4 = super().register(username, user_type).status_code
        self.assertEqual(500, status4,
                         "Failed! Preset user register again not failed in "
                         "test")

    def test_register_login(self):
        self.register_login(random_username(), 'Student')
        self.register_login(random_username(), 'Teacher')
        self.register_login(random_username(), 'SysUser')

    def test_emailverify(self):
        r = self.client.post('/auth/emailverify', data=json.dumps({
            'email_address': 'landcast@163.com',
            'username': 'landcast',
            'usertype': 'SysUser'
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))

    def test_smsverify(self):
        r = self.client.post('/auth/smsverify', data=json.dumps({
            'mobile_no': '13521273258',
            'country_code': '86'
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(r.get_data(as_text=True))

    def test_reset_password(self):
        username = random_username()
        super().register(username, 'Teacher')
        redis_store.set("VC:" + username, "000000")
        r = self.client.post('/auth/resetpassword', data=json.dumps({
            "username": username, "password": "123456",
            "verify_code": "000000"
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))


if __name__ == '__main__':
    unittest.main()
