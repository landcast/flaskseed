#!/usr/bin/env python
# from mockito import mock, verify
import json
import unittest
import sys
from datetime import datetime, timedelta

sys.path.append(".")
from unittests.test_base import TestBase, random_username


class RestLessTest(TestBase):
    auth_header = None
    student_id = 0
    token = None
    channel_name = None
    channel_id = 0
    enrollment_id = 0

    def get_student(self):
        end = (datetime.now() + timedelta(seconds=30)).isoformat()[:-3] + 'Z'
        start = (datetime.now() + timedelta(seconds=-30)).isoformat()[:-3] + 'Z'
        r = self.client.get('/api/v1/student', query_string="q=" + json.dumps({
            "filters": [
                {"name": "created_at", "op": "<=", "val": end},
                {"name": "created_at", "op": ">=", "val": start},
                {"name": "updated_by", "op": "==", "val": self.test_student}
            ]
        }),
                            content_type='application/json',
                            headers={self.config['JWT_HEADER']: self.token})
        self.app.logger.debug("status = " + str(r.status_code))
        self.assertEqual(200, r.status_code, 'get students failed')
        students = json.loads(r.get_data(as_text=True))['objects']
        self.app.logger.debug(len(students))
        self.assertGreater(len(students), 0, 'get students empty')
        self.app.logger.debug('student.id = ' + str(students[0]['id']))
        self.student_id = students[0]['id']

    def post_channel(self):
        '''
        Master record been posted by create db record could be done
        with multi associate records, in this case, the master
        channel could be created with multi enrollments creation together
        :return:
        '''
        self.channel_name = 'channel_' + str(datetime.now().timestamp())
        r = self.client.post('/api/v1/channel', data=json.dumps({
            "channel_desc": "test for channel with create enrollment",
            "channel_enrollments": [
                {
                    "created_at": "2018-05-21T13:27:09.908Z",
                    "student_id": self.student_id,
                    "updated_at": "2018-05-21T13:27:09.908Z",
                    "updated_by": "unittests"
                }
            ],
            "channel_name": self.channel_name,
            "channel_orders": [],
            "updated_by": self.test_student
        }), content_type='application/json',
                             headers={self.config['JWT_HEADER']: self.token})
        self.app.logger.debug("post status = " + str(r.status_code))
        self.app.logger.debug(r.get_data(as_text=True))
        # self.assertEqual(201, r.status_code,
        #                  "Return error")
        filters = {
            'filters': [
                {'name': 'channel_name', 'op': '==', 'val': self.channel_name}]
        }
        r = self.client.get('/api/v1/channel',
                            query_string='q=' + json.dumps(filters),
                            content_type='application/json',
                            headers={self.config['JWT_HEADER']: self.token})
        self.app.logger.debug("status = " + str(r.status_code))
        self.assertEqual(200, r.status_code, 'get posted channel failed')
        channels = json.loads(r.get_data(as_text=True))['objects']
        self.assertGreater(len(channels), 0, 'get channels empty')
        self.app.logger.debug(
            'channel.id = ' + str(channels[0]['id']) + ' channel.name = ' +
            channels[0]['channel_name'])
        self.channel_id = channels[0]['id']
        self.enrollment_id = channels[0]['channel_enrollments'][0]['id']

    def put_channel(self):
        '''
        from manual test, the put master action with cascade associate
        record, in this case is enrollment, can't do create, so associate
        record must also provide id property
        :return:
        '''
        self.app.logger.debug('self.channel_id: ' + str(self.channel_id))
        self.app.logger.debug('self.enrollment_id: ' + str(self.enrollment_id))
        r = self.client.put('/api/v1/channel/' + str(self.channel_id),
                            data=json.dumps({
                                "channel_desc": "calling put, change desc and "
                                                "add new enrollment",
                                "updated_by": self.test_student,
                                "channel_enrollments": [
                                    {
                                        "created_at":
                                            "2018-05-29T13:27:09.908Z",
                                        "student_id": self.student_id,
                                        "channel_id": self.channel_id,
                                        "id": self.enrollment_id,
                                        "updated_by": "put-action cascade"
                                    }
                                ],
                            }), content_type='application/json',
                            headers={self.config['JWT_HEADER']: self.token})
        self.app.logger.debug("channel put.status = " + str(r.status_code))
        self.app.logger.debug(r.get_data(as_text=True))
        # r = self.client.put('/api/v1/enrollment/' + str(self.enrollment_id),
        #                     data=json.dumps({
        #                         "created_at": "2018-05-29T13:27:09.908Z",
        #                         "student_id": self.student_id,
        #                         "channel_id": self.channel_id,
        #                         "updated_at": "2018-05-29T13:27:09.908Z",
        #                         "updated_by": "put-action alone"
        #                     }), content_type='application/json',
        #                     headers={self.config['JWT_HEADER']: self.token})
        # self.app.logger.debug("enrollment put.status = " + str(r.status_code))
        # self.app.logger.debug(r.get_data(as_text=True))

    def test_channel(self):
        self.get_student()
        self.post_channel()
        self.put_channel()


if __name__ == '__main__':
    unittest.main()
