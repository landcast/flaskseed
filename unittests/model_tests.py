#!/usr/bin/env python
# from mockito import mock, verify
import json
import unittest
import sys

sys.path.append(".")
from unittests.test_base import TestBase, random_username
from src.models import db, session_scope, Student, Notification
from src.models.common_models import row_dict


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

    def sql_query(self):
        with session_scope(db) as session:
            session.add_all([Notification(notice='test-1'),
                             Notification(notice='test-2',
                                          updated_by='rawsql')])
            session.flush()
            sql1 = "select id, notice, updated_at, updated_by " \
                   "from notification where notice like :x"
            r2 = session.execute(sql1, {'x': 'test-2'})
            row = r2.first()
            self.app.logger.debug('row=' + str(row))
            self.assertEqual(row['updated_by'], 'rawsql',
                             'check updated_at=rawsql')
            r3 = session.execute(sql1, {'x': 'test%'})
            for index, row in enumerate(r3.fetchall()):
                self.app.logger.debug('row ' + str(index) + ' = ' + str(row))
            # session.query(Notification).delete()

    def test_common(self):
        self.sql_check()
        self.sql_query()


if __name__ == '__main__':
    unittest.main()
