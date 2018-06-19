import json
import os
import sys

import unittest
from datetime import datetime, timedelta
from src.services import redis_store
from src.models import db, session_scope, SysControl, Curriculum, Subject, \
    SubjectCategory, Course, CourseSchedule, CourseClassroom, Courseware, \
    Teacher


def random_username():
    return 'u_' + str(datetime.now().timestamp())


class TestBase(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'app'):
            upper_path = os.path.abspath('.')
            sys.path.append(upper_path)
            from src import create_app
            from config import settings
            app = create_app(settings)
            self.client = app.test_client()
            self.app = app
            self.logger = app.logger
            self.config = app.config
            self.app_context = self.app.app_context()
            self.app_context.push()
            self.data_prepare()

    def tearDown(self):
        self.app_context.pop()
        pass

    def register(self, username, user_type):
        redis_store.set("VC:" + username, "000000")
        r = self.client.post('/auth/register', data=json.dumps({
            "username": username, "password": username,
            "usertype": user_type, "verify_code": "000000"
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))
        return r

    def login(self, username, user_type):
        r = self.client.post('/auth/login', data=json.dumps({
            "username": username, "password": username,
            "usertype": user_type
        }), content_type='application/json')
        self.app.logger.debug("status = " + str(r.status_code))
        self.app.logger.debug(json.loads(r.get_data(as_text=True)))
        return r

    def data_prepare(self):
        if not self.app.debug or self.app.config['ENV_NAME'] == 'prd':
            # only running in debug mode and not in prd environment
            return

        with session_scope(db) as session:
            pid = os.getpid()
            r = session.query(SysControl).filter(
                    SysControl.current_pid == pid).one_or_none()
            if r:
                # one process only run once
                return

            c_ap = Curriculum(full_name='AP', updated_by=str(pid), state=98)
            session.add(c_ap)
            c_ib = Curriculum(full_name='IB', updated_by=str(pid), state=98)
            session.add(c_ib)
            session.flush()
            self.logger.debug(c_ap)
            self.logger.debug(c_ib)
            sc = SubjectCategory(subject_category='history',
                                 updated_by=str(pid), state=98)
            session.add(sc)
            session.flush()
            self.logger.debug(sc)
            s_ap_history = Subject(subject_name='AP_history_grade_9',
                    curriculum_id=c_ap.id, state=98,
                    subject_category_id=sc.id, updated_by=str(pid))
            session.add(s_ap_history)
            s_ib_history = Subject(subject_name='IB_history_grade_9',
                                   curriculum_id=c_ib.id, state=98,
                                   subject_category_id=sc.id,
                                   updated_by=str(pid))
            session.add(s_ib_history)
            session.flush()
            self.logger.debug(s_ap_history)
            self.logger.debug(s_ib_history)
            teacher_name = random_username()
            self.register(teacher_name, 'Teacher')
            t = session.query(Teacher).filter(
                    Teacher.username == teacher_name).one_or_none()
            self.logger.debug(t)
            cs_ap_history = Course(course_name='T1_AP_history_grade_9',
                                   course_type=1,
                                   class_type=1, classes_number=80,
                                   state=98, price=900000,
                                   primary_teacher_id=t.id,
                                   subject_id=s_ap_history.id,
                                   updated_by=str(pid))
            session.add(cs_ap_history)
            cs_ib_history = Course(course_name='T1_IB_history_grade_9',
                                   course_type=2,
                                   class_type=1, classes_number=60,
                                   state=98, price=800000,
                                   primary_teacher_id=t.id,
                                   subject_id=s_ib_history.id,
                                   updated_by=str(pid))
            session.add(cs_ib_history)
            session.flush()
            self.logger.debug(cs_ap_history)
            self.logger.debug(cs_ib_history)
            cs_s_ap = CourseSchedule(start=datetime.now(), end=(
                    datetime.now() + timedelta(days=90)), state=98,
                                     course_id=cs_ap_history.id,
                                     updated_by=str(pid))
            session.add(cs_s_ap)
            cs_s_ib = CourseSchedule(start=datetime.now(), end=(
                    datetime.now() + timedelta(days=90)), state=98,
                                     course_id=cs_ib_history.id,
                                     updated_by=str(pid))
            session.add(cs_s_ib)
            session.flush()
            self.logger.debug(cs_s_ap)
            self.logger.debug(cs_s_ib)
            # finally add the control record of this pid
            sys_control = SysControl(current_pid=pid)
            session.add(sys_control)
            session.flush()
            self.logger.debug(sys_control)


if __name__ == '__main__':
    unittest.main()
