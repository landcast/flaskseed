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


class DuobeiLiveTest(TestBase):

    def test_duobei_live(self):
        '''
        String title(房间名称)
        String startTime（开始时间）
        int length（时长、分钟）
        int menNum（房间类型，//1：1对1，2：1对多，3：小班课程）
        :return: room

        '''
        start_time = datetime.now().isoformat()[:-3] + 'Z'
        r = requests.post(
            self.config['EP_LOCATION'] + self.config[
                'EP_LIVE_PATH'] + '/createRoom',
            data=json.dumps({
                'title': 'test extport live room',
                'startTime': start_time,
                'length': 60,
                'menNum': 1
            }), headers={'Content-type': 'application/json'})
        self.app.logger.debug(r.status_code)
        self.app.logger.debug(r.json())


if __name__ == "__main__":
    unittest.main()
