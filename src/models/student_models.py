import enum

from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String,Text, Integer, DateTime, Float, ForeignKey, \
    Enum
from enum import IntFlag

from src.models.course_models import CourseScheduleStatueEnum


class StudentSubject(EntityMixin, db.Model):
    optional = Column(Integer, nullable=False, comment='是否必修，1：选修，2；必修')
    desc = Column(String(2000), nullable=True, comment='英文描述信息')
    desc_zh = Column(String(2000), nullable=True, comment='中文描述信息')
    subject_name = Column(String(120), nullable=True, comment='科目名称')
    subject_type = Column(Integer,nullable=True, comment='1:学习科目，2：意向科目')
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    subjects = db.relationship('Student', backref='subjects', lazy=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=True)
    students = db.relationship('Subject', backref='students', lazy=True)


class StudySchedule(EntityMixin, db.Model):
    actual_start = Column(DateTime, nullable=False, comment='实际上课开始时间')
    actual_end = Column(DateTime, nullable=False, comment='实际上课结束时间')
    name = Column(String(50), nullable=False, comment='课程名称')
    study_state = Column(Integer, nullable=False, comment='学习状态，1：进行中，2：已经学完')
    student_evaluation = Column(Text, nullable=True, comment='学生评价')
    student_result = Column(String(2000), nullable=True, comment='学生结果反馈')
    teacher_evaluation = Column(Text, nullable=True, comment='教师评价')
    teacher_result = Column(String(2000), nullable=True, comment='教师结果反馈')
    homework = Column(String(255), nullable=True, comment='作业')
    test = Column(String(2000), nullable=True, comment='课后测试')
    student_score = Column(Float, nullable=True, comment='学生评分')
    teacher_score = Column(Float, nullable=True, comment='教师评分')
    order_id = Column(Integer, ForeignKey('order.id'),
                      nullable=False)
    schedule_type = Column(Enum(CourseScheduleStatueEnum), nullable=True,
                           comment='课程类型',
                           server_default=CourseScheduleStatueEnum.COMMON_CLASS.name)
    order_studys = db.relationship('Order', backref='order_studys', lazy=True)
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=False)
    course_schedule = db.relationship('CourseSchedule',
                                      backref='study_timetable', lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    study_courses = db.relationship('Student', backref='study_courses',
                                    lazy=True)
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=True)



class Homework(EntityMixin, db.Model):
    homework_type = Column(Integer, nullable=False, comment='作业类型1：教师留作业，2：学生完成作业')
    question_name = Column(String(100), nullable=True, comment='作业名称')
    question_text = Column(String(2000), nullable=True, comment='问题')
    question_attachment_url = Column(String(255), nullable=True, comment='问题附件地址可以多个，JSON')
    answer_text = Column(String(2000), nullable=True, comment='答案')
    answer_attachment_url = Column(String(255), nullable=True, comment='答案附件地址可以多个json')
    score = Column(Float, nullable=True, comment='分数')
    score_remark = Column(String(2000), nullable=True, comment='分数标记')
    score_reason = Column(String(2000), nullable=True, comment='分数得分原因')
    review_at = Column(DateTime, nullable=True, comment='点评时间')
    study_schedule_id = Column(Integer, ForeignKey('study_schedule.id'),
                               nullable=False)
    homeworks = db.relationship('StudySchedule', backref='homeworks',
                                lazy=True)


class StudyResultTypeEnum(enum.IntEnum):
    """
    SUMMARY:总结
    ACHIEVEMENT：成绩单
    """
    SUMMARY = 1
    ACHIEVEMENT = 2


class StudyResult(EntityMixin, db.Model):
    score = Column(Float, nullable=True, comment='分数')
    evaluation = Column(String(2000), nullable=True, comment='阶段性评价 json')
    score_type = Column(String(60), nullable=True, comment='得分类型')
    score_full_mark = Column(Float, nullable=True, comment="满分")
    score_reason = Column(String(2000), nullable=True, comment='得分原因')
    score_remark = Column(String(2000), nullable=True, comment='分数标记')
    score_comment = Column(String(2000), nullable=True, comment='分数确认')
    report_card_url = Column(String(200), nullable=True, comment='成绩单地址')
    report_card_name = Column(String(100), nullable=True, comment='成绩单名称')
    result_type = Column(Enum(StudyResultTypeEnum), nullable=True,
                         comment='结果类型',
                         server_default=StudyResultTypeEnum.
                         SUMMARY.name)
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
    form_no = Column(Integer, primary_key=True, comment='表单编号')
    form_submitted = Column(String(255), nullable=True, comment='表单提交内容-英文')
    provider = Column(String(255), nullable=True, comment='评估机构-英文')
    result = Column(String(4000), nullable=True, comment='评估结果-英文')
    form_submitted_zh = Column(String(255), nullable=True, comment='表单提交内容-中文')
    provider_zh = Column(String(255), nullable=True, comment='评估机构-中文')
    result_zh = Column(String(4000), nullable=True, comment='评估结果-中文')
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=True)
    subjects = db.relationship('Subject', backref='appraisals', lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    appraisals = db.relationship('Student', backref='appraisals', lazy=True)


class CourseAppraisal(EntityMixin, db.Model):
    """
    After study the whole course, record the study result and credit
    """
    course_study_result = Column(String(255), nullable=True, comment='试听英文反馈')
    course_study_result_zh = Column(String(255), nullable=True, comment='试听中文反馈')
    course_credit = Column(Float, nullable=True, comment='')
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_appraisals = db.relationship('Course', backref='study_results',
                                        lazy=True)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    course_results = db.relationship('Student', backref='course_appraisals',
                                     lazy=True)


class StudyAppointmentState(enum.IntEnum):
    """
    WRITE_APPOINTMENT :待预约
    WRITE_ACCEPT :待接受
    WRITE_CLASS :待上课
    FINISH :完成
    """
    WRITE_APPOINTMENT = 1
    WRITE_ACCEPT =2
    WRITE_CLASS =3
    FINISH =4


class StudyAppointment(EntityMixin, db.Model):
    student_requirements = Column(String(2000), nullable=True, comment='学生需求')
    apply_by = Column(String(50), nullable=True, comment='申请人')
    open_time_start = Column(DateTime, nullable=False, comment='试听开始时间')
    open_time_end = Column(DateTime, nullable=False, comment='试听结束时间')
    appointment_state = Column(Enum(StudyAppointmentState), nullable=False,
                               server_default=StudyAppointmentState.WRITE_APPOINTMENT.name)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)


class StudentState(IntFlag):
    """
    FRESH: 新注册
    BASIC_INFO：学生基本信息
    DISTRIBUTION_ADVISER:分配学生顾问
    PERFECT_INFORMATION：完善信息
    DISTRIBUTION_HEADMASTER:待分配学生班主任
    HAVE_HEADMASTER:分配学生班主任
    NOORDER:未下订单
    INSTUDY: 付费上课
    GRADUATED: 已经毕业
    INVALID:无效
    """
    FRESH = 1
    BASIC_INFO = 2
    DISTRIBUTION_ADVISER = 3
    PERFECT_INFORMATION = 4
    DISTRIBUTION_HEADMASTER = 5
    HAVE_HEADMASTER = 6
    NOORDER = 7
    INSTUDY = 8
    GRADUATED = 9

    INVALID=99

class Student(UserBaseMixin, db.Model):
    state = Column(Enum(StudentState), nullable=False,
                   server_default=StudentState.FRESH.name)
    level = Column(String(50), nullable=True, comment='等级')
    nation = Column(String(50), nullable=True, comment='国家')
    city = Column(String(50), nullable=True, comment='城市')
    grade = Column(Integer, nullable=True, comment='当前学校班级')
    read_country = Column(String(100), nullable=True, comment='在读国家')
    read_province = Column(String(100), nullable=True, comment='在读省/州')
    read_school = Column(String(100), nullable=True, comment='在读学校英文')
    read_school_zh = Column(String(100), nullable=True, comment='在读学校中文')
    interest = Column(String(1000), nullable=True, comment='兴趣爱好英文')
    interest_zh = Column(String(1000), nullable=True, comment='兴趣爱好中文')
    award = Column(String(500), nullable=True, comment='获得奖项英文')
    award_zh = Column(String(500), nullable=True, comment='获得奖项中文')
    go_abroad = Column(String(5), nullable=True, comment='是否出国YES/NO')
    go_abroad_at = Column(DateTime, nullable=True, comment='预计出国时间')
    go_abroad_country = Column(String(50), nullable=True, comment='预计出国国家')
    go_abroad_province = Column(String(50), nullable=True, comment='预计出国国家省/州')
    overseas = Column(String(500), nullable=True, comment='海外经历英文')
    overseas_zh = Column(String(500), nullable=True, comment='海外经历中文中文')
    english = Column(String(500), nullable=True, comment='英语情况英文')
    english_zh = Column(String(500), nullable=True, comment='英语情况中文')
    exam_results = Column(String(500), nullable=True, comment='考试与成绩英文')
    exam_results_zh = Column(String(500), nullable=True, comment='考试与成绩中文')
    parent = Column(String(50), nullable=True, comment='家长姓名')
    parent_mobile = Column(String(20), nullable=True, comment='家长联系电话')
    parent_email = Column(String(60), nullable=True, comment='家长邮件')
    parent_role = Column(String(20), nullable=True, comment='家长称谓')
    remark = Column(String(500), nullable=True, comment='标注信息')
    consultant_id = Column(Integer, ForeignKey('sys_user.id'),
                           nullable=True,
                           comment='sales person provide consultant'
                                   ' services or other customer '
                                   'services')
    consultants = db.relationship('SysUser',
                                  backref='sales_customers',
                                  lazy=True, foreign_keys=consultant_id)
    student_helper_id = Column(Integer, ForeignKey('sys_user.id'),
                               nullable=True,
                               comment='customer services providers')
    student_helpers = db.relationship('SysUser',
                                      backref='student_helpers',
                                      lazy=True,
                                      foreign_keys=student_helper_id)
    channel_id = Column(Integer, ForeignKey('channel.id'),
                        nullable=True)


class StudentRequirements(EntityMixin, db.Model):
    content = Column(String(1000),nullable=True, comment='英文内容')
    content_zh = Column(String(1000),nullable=True, comment='中文内容')
    translate_by = Column(Integer,nullable=True, comment='翻译人')
    translate_at = Column(DateTime, nullable=True, comment='翻译时间')
    student_id = Column(db.Integer, db.ForeignKey('student.id'),
                        nullable=False)
    student_requirements = db.relationship('Student', backref='studentrequirements', lazy=True)


class StudentSubjectOptional(IntFlag):
    """
    ELECTIVE_COURSE：选修课程
    COMPULSORY_COURSE:必修课程
     """
    ELECTIVE_COURSE = 1
    COMPULSORY_COURSE = 2

class StudyScheduleStudyState(IntFlag):
    """
   ONGOING：进行中
   COMPLETED:已经完成
    """
    ONGOING = 1
    COMPLETED = 2