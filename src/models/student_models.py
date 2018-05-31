from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, \
    Enum
from enum import IntFlag


class StudentSubject(EntityMixin, db.Model):
    optional = Column(Integer, nullable=False)
    desc = Column(String(255), nullable=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    subjects = db.relationship('Student', backref='subjects', lazy=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=False)
    students = db.relationship('Subject', backref='students', lazy=True)


class StudySchedule(EntityMixin, db.Model):
    actual_start = Column(DateTime, nullable=False)
    actual_end = Column(DateTime, nullable=False)
    study_state = Column(Integer, nullable=False)
    evaluation = Column(String(255), nullable=True)
    result = Column(String(255), nullable=True)
    homework = Column(String(255), nullable=True)
    test = Column(String(255), nullable=True)
    order_id = Column(Integer, ForeignKey('order.id'),
                      nullable=False)
    order_studys = db.relationship('Order', backref='order_studys', lazy=True)
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=False)
    course_schedule = db.relationship('CourseSchedule',
                                      backref='study_timetable', lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    study_courses = db.relationship('Student', backref='study_courses',
                                    lazy=True)


class Homework(EntityMixin, db.Model):
    homework_type = Column(Integer, nullable=False)
    question_text = Column(String(2000), nullable=True)
    question_attachment_url = Column(String(255), nullable=True)
    answer_text = Column(String(2000), nullable=True)
    answer_attachment_url = Column(String(255), nullable=True)
    score = Column(Float, nullable=True)
    score_remark = Column(String(2000), nullable=True)
    score_reason = Column(String(2000), nullable=True)
    study_schedule_id = Column(Integer, ForeignKey('study_schedule.id'),
                               nullable=False)
    homeworks = db.relationship('StudySchedule', backref='homeworks',
                                lazy=True)


class StudyResult(EntityMixin, db.Model):
    score = Column(Float, nullable=True)
    score_type = Column(String(60), nullable=True)
    score_full_mark = Column(Float, nullable=True, comment="满分")
    score_reason = Column(String(2000), nullable=True)
    score_remark = Column(String(2000), nullable=True)
    score_comment = Column(String(2000), nullable=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    student_study_results = db.relationship('Student', backref='study_results',
                                            lazy=True)
    course_exam_id = Column(Integer, ForeignKey('course_exam.id'),
                            nullable=False)
    course_exam_results = db.relationship('CourseExam',
                                          backref='course_exam_results',
                                          lazy=True)


class StudentAppraisal(EntityMixin, db.Model):
    form_no = Column(Integer, primary_key=True)
    form_submitted = Column(String(255), nullable=True)
    provider = Column(String(255), nullable=True)
    result = Column(String(4000), nullable=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=True)
    subjects = db.relationship('Subject', backref='appraisals', lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    appraisals = db.relationship('Student', backref='appraisals', lazy=True)


class CourseAppraisal(EntityMixin, db.Model):
    '''
    After study the whole course, record the study result and credit
    '''
    course_study_result = Column(String(255), nullable=True)
    course_credit = Column(Float, nullable=True)
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_appraisals = db.relationship('Course', backref='study_results',
                                        lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    course_results = db.relationship('Student', backref='course_appraisals',
                                     lazy=True)


class StudyAppointment(EntityMixin, db.Model):
    student_requirements = Column(String(2000), nullable=False)
    course_appointment_id = Column(Integer, ForeignKey('course_appointment.id'),
                                   nullable=False)
    course_appointments = db.relationship('CourseAppointment',
                                          backref='student_appointments',
                                          lazy=True)


class StudentState(IntFlag):
    """
    FRESH: 新注册
    TAKEN_TRAIL: 上过试听课
    INSTUDY: 付费上课
    """
    FRESH = 1
    TAKEN_TRAIL = 2
    INSTUDY = 4


class Student(UserBaseMixin, db.Model):
    state = Column(Enum(StudentState), nullable=False,
                   server_default=StudentState.FRESH.name)
    level = Column(String(50), nullable=True)
    nation = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    cur_school = Column(String(50), nullable=True)
    grade = Column(Integer, nullable=True)
    requirements = Column(String(2000), nullable=True)
    parent = Column(String(50), nullable=True)
    parent_mobile = Column(String(20), nullable=True)
    parent_email = Column(String(60), nullable=True)
    parent_role = Column(String(20), nullable=True)
    consultant_id = Column(Integer, ForeignKey('sys_user.id'),
                           nullable=True,
                           comment='sales person provide consultant'
                                   ' service or other customer '
                                   'service')
    consultants = db.relationship('SysUser',
                                  backref='sales_customers',
                                  lazy=True, foreign_keys=consultant_id)
    student_helper_id = Column(Integer, ForeignKey('sys_user.id'),
                               nullable=True,
                               comment='customer service providers')
    student_helpers = db.relationship('SysUser',
                                      backref='student_helpers',
                                      lazy=True,
                                      foreign_keys=student_helper_id)
