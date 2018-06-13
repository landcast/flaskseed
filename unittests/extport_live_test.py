#!/usr/bin/env python
from datetime import datetime
# from mockito import mock, verify
import os
import unittest
import sys

sys.path.append(".")
from unittests.test_base import TestBase
from src.services.live_service import create_room, edit_room, delete_room, \
    enter_room, upload_doc, attach_doc, preview_doc, remove_doc
from src.models import db, session_scope, CourseSchedule


class DuobeiLiveTest(TestBase):

    def test_duobei_live(self):
        '''
        Test for services.live_service
        '''
        url = 'http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/pdf/' \
              'dds-product-introduction-intl-zh-2018-03-30.pdf'
        start_time = datetime.now().isoformat()[:-3] + 'Z'
        self.app.logger.debug(start_time)
        with session_scope(db) as session:
            cs = session.query(CourseSchedule).filter(
                    CourseSchedule.updated_by == os.getpid()).first()
            if cs:
                r = create_room('86-13521273258', cs.id, 'test room', 60)
                self.app.logger.debug(r)
                self.assertIsNotNone(r, 'create room not return room for succ')
                room_id = r['roomId']
                r = edit_room('86-13521273258', room_id, 'edit room', 90)
                self.app.logger.debug(r)
                r = enter_room('86-13521273258', room_id, 'Tom')
                self.app.logger.debug(r)
                self.assertIsNotNone(r, 'enter room not return url')
                # test upload course ware
                r = upload_doc('86-13521273258', url,
                               'python-consul.pdf', cs.course_id)
                self.app.logger.debug(r)
                self.assertIsNotNone(r, 'upload_doc not return ware_uid')
                # attach uploaded course ware with created room
                ware_uid = r
                r = attach_doc('86-13521273258', room_id, ware_uid)
                self.app.logger.debug(r)
                self.assertEqual(None, r, 'attach_doc not return None for succ')
                # get preview document url from ware_uid
                self.app.logger.debug('ware_uid: ' + ware_uid)
                r = preview_doc('86-13521273258', ware_uid)
                self.app.logger.debug(r)
                self.assertIsNotNone(r, 'preview_doc not return url for succ')
                # remove document from room
                r = remove_doc('86-13521273258', room_id, ware_uid)
                self.app.logger.debug(r)
                # self.assertEqual(None, r, 'remove_doc not return None for succ')
                # finally delete class room
                r = delete_room('86-13521273258', room_id)
                self.app.logger.debug(r)
                self.assertEqual(None, r,
                                 'delete_room not return None for succ')


if __name__ == "__main__":
    unittest.main()
