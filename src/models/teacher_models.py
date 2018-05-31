from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, \
    Enum
from enum import IntFlag


class Certificate(EntityMixin, db.Model):
    cert_name = Column(db.String(120), nullable=False)
    cert_desc = Column(db.String(120), nullable=True)
    cert_level = Column(db.String(120), nullable=True)
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='certificates', lazy=True)


class TeacherSubject(EntityMixin, db.Model):
    advantage = Column(String(120), nullable=False)
    desc = Column(String(255), nullable=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'),
                        nullable=False)
    subjects = db.relationship('Teacher', backref='subjects', lazy=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=False)
    teachers = db.relationship('Subject', backref='teachers', lazy=True)


class Interview(EntityMixin, db.Model):
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False)
    reason = Column(String(2000), nullable=True,
                    comment="state change to history, record change reason")
    result = Column(String(2000), nullable=True)
    interviewer_id = Column(db.Integer, db.ForeignKey('sys_user.id'),
                            nullable=False)
    interviewers = db.relationship('SysUser', backref='interviewers', lazy=True)
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='interviews', lazy=True)


class TeacherState(IntFlag):
    """
    RECRUIT: 招募完成
    BG_CHECK_PASS: 认证完成
    INTERVIEW_PASS: 面试完成
    TRAIL_LECTURE_APPOINTMENT: 约定试课
    TRAIL_LECTURE_PASS: 试课通过
    CONTRACTOR: 签约完成
    TEACHING: 教课中
    """
    RECRUIT = 1
    BG_CHECK_PASS = 2
    INTERVIEW_PASS = 4
    TRAIL_LECTURE_APPOINTMENT = 8
    TRAIL_LECTURE_PASS = 16
    CONTRACTOR = 32
    TEACHING = 64


class Teacher(UserBaseMixin, db.Model):
    state = Column(Enum(TeacherState), nullable=False,
                   server_default=TeacherState.RECRUIT.name)
    level = Column(String(50), nullable=True)
    nation = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    timezone = Column(Integer, nullable=True)
    contract = Column(String(255), nullable=True)
    cur_school = Column(String(50), nullable=True)
    race = Column(String(120), nullable=True)
    ancestral = Column(String(120), nullable=True,
                       comment="e.g. egyptian american")
    contract_url = Column(String(255), nullable=True)
    contract_dollar_price = Column(Float, nullable=True,
                                   comment="dollar price for this teacher")
