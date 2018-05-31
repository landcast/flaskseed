#!/usr/bin/env python
# from mockito import mock, verify
import json
import unittest
import sys

sys.path.append(".")
from unittests.test_base import TestBase, random_username
from src.models import db, session_scope, Student, Notification


class ModelTest(TestBase):

    def sql_check(self):
        todo_user = random_username()
        json.loads(
            super().register(todo_user, 'Student').get_data(
                as_text=True))
        with session_scope(db) as session:
            r1 = session.execute("select * from student")
            row1 = r1.first()
            self.assertIsNotNone(row1,
                                 "After student register, no record found for "
                                 "student")
            r2 = session.add_all([Notification(notice='meeting today'),
                                  Notification(notice='meeting cancel')])
            self.app.logger.debug('r2=' + str(r2))
            r3 = session.query(Notification).delete()
            self.app.logger.debug('r3=' + str(r3))
            r4 = session.query(Notification).first()
            self.app.logger.debug('r4=' + str(r4))
            self.assertIsNone(r4, "After delete all, first should return None")
            r5 = session.query(Notification).one_or_none()
            self.app.logger.debug('r5=' + str(r5))

    def test_common(self):
        self.sql_check()


if __name__ == '__main__':
    unittest.main()
