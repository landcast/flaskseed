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
    start = Column(DateTime, nullable=True, comment='预计面试开始时间')
    end = Column(DateTime, nullable=True, comment='预计面试结束时间')
    state = Column(Integer, nullable=False, comment='1：未面试，2：已经面试，3：取消')
    reason = Column(String(2000), nullable=True,
                    comment="state change to history, record change reason")
    result = Column(String(2000), nullable=True, comment='面试结果')
    set_time = Column(String(2000), nullable=True, comment='设置面试时间 json')
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
    WAITE_FOR_CONTRACT:待签约，
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
    WAITE_FOR_CONTRACT = 11
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
    skype_account = Column(String(50), nullable=True, comment='skype账号')
    degree = Column(String(50), nullable=True, comment='大专学历 college_graduate，本科学历  university_diploma，'
                                                       '学士学位  bachelor_degree，硕士学位  master_degree，博士学位  doctor_degree，'
                                                       '博士后  post-doctoral，other 其他')
    nation = Column(String(50), nullable=True, comment='国家国际代码')
    country = Column(String(50), nullable=True, comment='国家')
    province = Column(String(50), nullable=True, comment='省/州')
    city = Column(String(50), nullable=True, comment='城市')
    street = Column(String(200), nullable=True, comment='街道')
    timezone = Column(Integer, nullable=True, comment='时区')
    zipone = Column(Integer, nullable=True, comment='时区代码')
    contract = Column(String(255), nullable=True, comment='合同信息')
    cur_school = Column(String(50), nullable=True, comment='当前工作学校')
    cur_zone = Column(String(50), nullable=True, comment='当前地区')
    cur_grade = Column(String(100), nullable=True, comment='当前教授年级')
    cur_country = Column(String(100), nullable=True, comment='当前任职地区')
    cur_province = Column(String(100), nullable=True, comment='当前工作省/州')
    graduation_school = Column(String(50), nullable=True, comment='毕业最高学校')
    education_history = Column(String(1000), nullable=True, comment='上学历史 json')
    teaching_history = Column(String(1000), nullable=True, comment='教学历史 json')
    about_me = Column(String(1000), nullable=True, comment='自我介绍')
    race = Column(String(120), nullable=True, comment='种族')
    teacher_age = Column(Integer, nullable=True, comment='教龄')
    resume_url = Column(String(100), nullable=True, comment='简历url')
    seniority_url = Column(String(100), nullable=True,
                   comment="教师资格证明url JSON")
    award_url = Column(String(1000), nullable=True,
                           comment="获奖文件地址 JSON")
    ancestral = Column(String(120), nullable=True,
                       comment="原籍")
    contract_url = Column(String(255), nullable=True, comment='合同下载地址')
    contract_dollar_price = Column(Float, nullable=True,
                                   comment="dollar price for this teacher")


class TeacherTime(EntityMixin, db.Model):
    week = Column(db.String(10), nullable=False, comment='星期几，1，2，3，4，5，6，7')
    end = Column(DateTime, nullable=False, comment='可授课结束时间')
    start = Column(Integer, nullable=False, comment='可以授课开始时间')
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='teachertime', lazy=True)


class TeacherHistory(EntityMixin, db.Model):
    subject_id = Column(Integer,nullable=True, comment='可教授的科目id')
    subject_name = Column(Integer,nullable=True, comment='可教授的科目名称')
    grade = Column(Integer,nullable=True, comment='Kindergarten:幼儿园，primary_school:小学，junior_middle_school:初中，'
                                                  'high_school:高中，university：大学，adult：成人，other:其他 JSON串')
    type = Column(Integer, nullable=False, comment='类型，1：可以交的科目，2：现在交的科目')
    teacher_id = Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)
    teachers = db.relationship('Teacher', backref='teacherhistory', lazy=True)


class InterviewState(IntFlag):
    """
    WRITE_APPOINT:待预约
    NO_INTERVIEW:未面试
    ALREADY_INTERVIEW:已经面试
    CANCEL:取消
    NO_COMPLETED:未完成
    WRITE_ANSWER:等待答复、
    WRITE_CONFIRM:等待确认时间、
    UNDETERMINED:待定、
    INTERVIEW_PASS:面试结果通过，
    INTERVIEW_ERROR:面试结果失败，
    EFFECTIVE:有效
    INVALID:无效
    """
    WRITE_APPOINT = 1
    NO_INTERVIEW =2
    ALREADY_INTERVIEW = 3
    CANCEL = 4
    NO_COMPLETED=5
    WRITE_ANSWER=6
    WRITE_CONFIRM=7
    UNDETERMINED=8
    INTERVIEW_PASS=9
    INTERVIEW_ERROR=10
    EFFECTIVE = 98
    INVALID = 99

