import json
import subprocess
import sys
import unittest
sys.path.append('.')
from integrationtests import random_username, TestBase, redis_store, logger


class AuthCurlTest(TestBase):

    def test_register(self):
        username = random_username()
        status, output = super().register(username, 'SysUser')
        self.assertTrue('200 OK' in output, 'expect http status return 200')
        self.assertEqual(status, 0)
        print(output)
        username = random_username()
        output = super().json_register(username, 'SysUser')
        print(output)


if __name__ == "__main__":
    unittest.main()
