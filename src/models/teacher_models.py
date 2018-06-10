from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, \
    Enum
from enum import IntFlag


class Certificate(EntityMixin, db.Model):
    cert_name = Column(db.String(120), nullable=False, comment='证书英文名称')
    cert_desc = Column(db.String(120), nullable=True, comment='证书英文描述')
    cert_name_zh = Column(db.String(120), nullable=True, comment='证书中文名称')
    cert_desc_zh = Column(db.String(120), nullable=True, comment='证书中文描述')
    cert_level = Column(db.String(120), nullable=True, comment='证书级别')
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='certificates', lazy=True)


class TeacherSubject(EntityMixin, db.Model):
    advantage = Column(String(120), nullable=False, comment='教师特点英文')
    desc = Column(String(255), nullable=True, comment='教师描述英文')
    advantage_zh = Column(String(120), nullable=True, comment='教师特点英文')
    desc_zh = Column(String(255), nullable=True, comment='教师描述中文')
    teacher_id = Column(Integer, ForeignKey('teacher.id'),
                        nullable=False)
    subjects = db.relationship('Teacher', backref='subjects', lazy=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=False)
    teachers = db.relationship('Subject', backref='teachers', lazy=True)


class Interview(EntityMixin, db.Model):
    start = Column(DateTime, nullable=False, comment='预计面试开始时间')
    end = Column(DateTime, nullable=False, comment='预计面试结束时间')
    state = Column(Integer, nullable=False, comment='面试状态，4：已预约，10，待面试')
    reason = Column(String(2000), nullable=True,
                    comment="state change to history, record change reason")
    result = Column(String(2000), nullable=True, comment='面试结果')
    interviewer_id = Column(db.Integer, db.ForeignKey('sys_user.id'),
                            nullable=False)
    interviewers = db.relationship('SysUser', backref='interviewers', lazy=True)
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='interviews', lazy=True)


class TeacherState(IntFlag):
    """
    RECRUIT：新用户，
    BASIC_INFO：填写基本信息，
    WAIT_FOR_CHECK:待审核，
    CHECK_PASS:审核通过(待预约)、
    CHECK_ERROR:审核未通过，
    WAIT_FOR_INTERVIEW：已预约(待面试)，
    INTERVIEW_PASS:面试结果通过(待签约)，
    INTERVIEW_ERROR:面试结果失败，
    CONTRACTOR:已签约，
    WAIT_FOR_TRAIN:待预约培训试讲，
    TRAIN_PASS:培训试讲结果成功，
    TRAIN_ERROR:培训试讲结果失败
    WORKING:在岗，
    NO_WORK:未在岗
     INVALID：无效
    """
    RECRUIT = 1
    BASIC_INFO = 2
    WAIT_FOR_CHECK = 3
    CHECK_PASS = 4
    CHECK_ERROR = 5
    WAIT_FOR_INTERVIEW = 10
    INTERVIEW_PASS = 11
    INTERVIEW_ERROR = 12
    CONTRACTOR = 20
    WAIT_FOR_TRAIN = 30
    TRAIN_PASS = 31
    TRAIN_ERROR = 32
    WORKING = 80
    NO_WORK = 81
    INVALID = 99


class Teacher(UserBaseMixin, db.Model):
    state = Column(Enum(TeacherState), nullable=False,
                   server_default=TeacherState.RECRUIT.name)
    level = Column(String(50), nullable=True, comment='教师级别')
    nation = Column(String(50), nullable=True, comment='国家')
    city = Column(String(50), nullable=True, comment='城市')
    timezone = Column(Integer, nullable=True, comment='时区')
    contract = Column(String(255), nullable=True, comment='合同信息')
    cur_school = Column(String(50), nullable=True, comment='当前工作学校')
    race = Column(String(120), nullable=True, comment='')
    ancestral = Column(String(120), nullable=True,
                       comment="e.g. egyptian american")
    contract_url = Column(String(255), nullable=True, comment='合同下载地址')
    contract_dollar_price = Column(Float, nullable=True,
                                   comment="dollar price for this teacher")


class InterviewState(IntFlag):
    """
    CHECK_PASS:审核通过(待预约)、
    WAIT_FOR_INTERVIEW：已预约(待面试)，
    """
    CHECK_PASS = 4
    WAIT_FOR_INTERVIEW = 10

