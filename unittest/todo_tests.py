#!/usr/bin/env python
# from mockito import mock, verify
import json
import unittest
import sys

sys.path.append(".")
from unittest.test_base import TestBase, random_username


class TodoTest(TestBase):

    def add_todo(self, action):
        todo_user = random_username()
        auth_header = json.loads(
            super().register(todo_user, 'Student').get_data(as_text=True))
        token = auth_header[self.config['JWT_HEADER']]
        r = self.client.put('/todos/todo1', data={
            'data': action
        }, headers={self.config['JWT_HEADER']: token})
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))
        self.assertEqual(201, r.status_code,
                         "Return error")
        r = self.client.get('/todos/todo1',
                            headers={self.config['JWT_HEADER']: token})
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(r.get_data(as_text=True))

    def test_todo(self):
        self.add_todo('study python')


if __name__ == '__main__':
    unittest.main()
