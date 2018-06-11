from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, \
    Enum
from enum import IntFlag


class StudentSubject(EntityMixin, db.Model):
    optional = Column(Integer, nullable=False, comment='是否必修，1：选修，2；必修')
    desc = Column(String(2000), nullable=True, comment='英文描述信息')
    desc_zh = Column(String(2000), nullable=True, comment='中文描述信息')
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    subjects = db.relationship('Student', backref='subjects', lazy=True)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=False)
    students = db.relationship('Subject', backref='students', lazy=True)


class StudySchedule(EntityMixin, db.Model):
    actual_start = Column(DateTime, nullable=False, comment='实际上课开始时间')
    actual_end = Column(DateTime, nullable=False, comment='实际上课结束时间')
    study_state = Column(Integer, nullable=False, comment='学习状态，1：进行中，2：已经学完')
    evaluation = Column(String(255), nullable=True, comment='评价')
    result = Column(String(255), nullable=True, comment='结果反馈')
    homework = Column(String(255), nullable=True, comment='作业')
    test = Column(String(255), nullable=True, comment='课后测试')
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
    homework_type = Column(Integer, nullable=False, comment='作业类型1：教师留作业，2：学生完成作业')
    question_text = Column(String(2000), nullable=True, comment='问题')
    question_attachment_url = Column(String(255), nullable=True, comment='问题附件地址可以多个，JSON')
    answer_text = Column(String(2000), nullable=True, comment='答案')
    answer_attachment_url = Column(String(255), nullable=True, comment='答案附件地址可以多个json')
    score = Column(Float, nullable=True, comment='分数')
    score_remark = Column(String(2000), nullable=True, comment='分数标记')
    score_reason = Column(String(2000), nullable=True, comment='分数得分原因')
    study_schedule_id = Column(Integer, ForeignKey('study_schedule.id'),
                               nullable=False)
    homeworks = db.relationship('StudySchedule', backref='homeworks',
                                lazy=True)


class StudyResult(EntityMixin, db.Model):
    score = Column(Float, nullable=True, comment='分数')
    score_type = Column(String(60), nullable=True, comment='得分类型')
    score_full_mark = Column(Float, nullable=True, comment="满分")
    score_reason = Column(String(2000), nullable=True, comment='得分原因')
    score_remark = Column(String(2000), nullable=True, comment='分数标记')
    score_comment = Column(String(2000), nullable=True, comment='分数确认')
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


class StudyAppointment(EntityMixin, db.Model):
    student_requirements = Column(String(2000), nullable=False, comment='学生需求')
    course_appointment_id = Column(Integer, ForeignKey('course_appointment.id'),
                                   nullable=False)
    course_appointments = db.relationship('CourseAppointment',
                                          backref='student_appointments',
                                          lazy=True)


class StudentState(IntFlag):
    """
    FRESH: 新注册
    BASIC_INFO：学生基本信息
    DISTRIBUTION_ADVISER:分配学生顾问
    PERFECT_INFORMATION：完善信息
    DISTRIBUTION_HEADMASTER:分配学生班主任
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
    cur_school = Column(String(50), nullable=True, comment='当前学校')
    grade = Column(Integer, nullable=True, comment='当前学校班级')
    requirements = Column(String(2000), nullable=True, comment='学生需求英文，可能是JSON需注意')
    requirements_zh = Column(String(2000), nullable=True, comment='学生徐需求中文，可能是JSON需注意')
    parent = Column(String(50), nullable=True, comment='')
    parent_mobile = Column(String(20), nullable=True, comment='')
    parent_email = Column(String(60), nullable=True, comment='')
    parent_role = Column(String(20), nullable=True, comment='')
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