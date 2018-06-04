#!/usr/bin/env python
from datetime import datetime
# from mockito import mock, verify
import unittest
import sys

sys.path.append(".")
from unittests.test_base import TestBase, random_username
from src.service.live_service import create_room


class DuobeiLiveTest(TestBase):

    def test_duobei_live(self):
        '''
        Test for service.live_service.create_room
        '''
        start_time = datetime.now().isoformat()[:-3] + 'Z'
        self.app.logger.debug(start_time)
        r = create_room('86-13521273258', 'test room', 60)
        self.app.logger.debug(r)
        self.assertEqual(0, r['code'], 'not return 0 for succ')


if __name__ == "__main__":
    unittest.main()
