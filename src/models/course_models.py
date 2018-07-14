import enum
from src.models.common_models import db, EntityMixin
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum


class Curriculum(EntityMixin, db.Model):
    full_name = Column(String(120), nullable=False, comment='课程全名-英文')
    desc = Column(String(255), nullable=True, comment='课程描述-英文')
    cover_url = Column(String(255), nullable=True, comment='封面地址')
    prerequisite = Column(String(255), nullable=True,
                          comment='学习本门课程先决条件-英文')
    language_requirement = Column(String(255), nullable=True,
                                  comment='语言条件-英文')

    full_name_zh = Column(String(120), nullable=True, comment='课程全名-中文')
    desc_zh = Column(String(255), nullable=True, comment='课程描述-中文')
    prerequisite_zh = Column(String(255), nullable=True,
                             comment='学习本门课程先决条件-中文')
    language_requirement_zh = Column(String(255), nullable=True,
                                     comment='语言条件-中文')
    state = Column(Integer, nullable=False, comment='有效：98，无效：99')


class SubjectCategory(EntityMixin, db.Model):
    subject_category = Column(String(120), nullable=False,
                              comment='科目类别英文名称-英文')
    subject_category_zh = Column(String(120), nullable=True,
                                 comment='科目类别中文名称-中文')
    desc = Column(String(255), nullable=True, comment='课程描述-英文')
    desc_zh = Column(String(255), nullable=True, comment='课程描述-中文')
    cover_url = Column(String(255), nullable=True, comment='封面地址')
    state = Column(Integer, nullable=False, comment='有效：98，无效：99')
    curriculum_id = Column(Integer, ForeignKey('curriculum.id'),
                           nullable=True)


class Subject(EntityMixin, db.Model):
    subject_name = Column(String(120), nullable=False, comment='学科名称-英文')
    subject_desc = Column(String(120), nullable=True, comment='学科描述-英文')
    subject_open_grade = Column(String(120), nullable=True,
                                comment='学科年级-英文')
    subject_requirements = Column(String(120), nullable=True,
                                  comment='学科要求-英文')

    subject_name_zh = Column(String(120), nullable=True, comment='学科名称-中文')
    subject_desc_zh = Column(String(120), nullable=True, comment='学科描述-中文')
    subject_open_grade_zh = Column(String(120), nullable=True,
                                   comment='学科年级-中文')
    subject_requirements_zh = Column(String(120), nullable=True,
                                     comment='学科要求-中文')
    cover_url = Column(String(255), nullable=True, comment='封面地址')
    state = Column(Integer, nullable=False, comment='有效：98，无效：99')
    curriculum_id = Column(Integer, ForeignKey('curriculum.id'),
                           nullable=True)
    subject_of_curriculum = db.relationship('Curriculum',
                                            backref='curriculum_subjects',
                                            lazy=True)
    subject_category_id = Column(Integer, ForeignKey('subject_category.id'),
                                 nullable=True)
    subject_of_category = db.relationship('SubjectCategory',
                                          backref='category_subjects',
                                          lazy=True)


class Course(EntityMixin, db.Model):
    course_name = Column(String(120), nullable=False, comment='课程名称-英文')
    course_name_zh = Column(String(120), nullable=True, comment='课程名称-中文')
    course_type = Column(Integer, nullable=False,
                         comment='全部：1，在线：2，公开：3')
    class_type = Column(Integer, nullable=False,
                        comment='enum, e.g. 1 v 1, 1 v 4, 1 v n')
    classes_number = Column(Integer, nullable=False, comment='课节数')
    open_grade = Column(String(120), nullable=True, comment='开设年级')
    course_desc = Column(String(120), nullable=True, comment='课程描述-英文')
    course_desc_zh = Column(String(120), nullable=True, comment='课程描述-中文')
    difficult_level = Column(Integer, nullable=True, comment='困难级别')
    critical_level = Column(Integer, nullable=True, comment='重要程度')
    start = Column(DateTime, nullable=True, comment='上课开始时间')
    end = Column(DateTime, nullable=True, comment='上课结束时间')
    course_requirements = Column(String(120), nullable=True,
                                 comment='课程要求-英文')
    course_requirements_zh = Column(String(120), nullable=True,
                                    comment='课程要求-中文')
    state = Column(Integer, nullable=False, comment='有效：98，无效：99')
    price = Column(Integer, nullable=False, comment='金额')
    primary_teacher_id = Column(Integer, ForeignKey('teacher.id'),
                                nullable=False)
    primary_teacher = db.relationship('Teacher', backref='primary_courses',
                                      lazy=True,
                                      foreign_keys=primary_teacher_id)
    assist_teacher_id = Column(Integer, ForeignKey('teacher.id'),
                               nullable=True)
    assist_teacher = db.relationship('Teacher', backref='assist_courses',
                                     lazy=True, foreign_keys=assist_teacher_id)
    subject_id = Column(Integer, ForeignKey('subject.id'),
                        nullable=False)
    courses_of_subject = db.relationship('Subject', backref='courses',
                                         lazy=True)


class CourseExam(EntityMixin, db.Model):
    start = Column(DateTime, nullable=False, comment='考试开始见')
    end = Column(DateTime, nullable=False, comment='考试结束时间')
    state = Column(Integer, nullable=False, comment='状态参考枚举值')
    exam_form = Column(String(255), nullable=True, comment='考试来源')
    exam_desc = Column(String(255), nullable=False, comment='考试描述')
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_schedules = db.relationship('Course', backref='course_exams',
                                       lazy=True)


class CourseSchedule(EntityMixin, db.Model):
    start = Column(DateTime, nullable=False, comment='开始时间')
    end = Column(DateTime, nullable=False, comment='结束时间')
    state = Column(Integer, nullable=False, comment='状态参考枚举值')
    name = Column(String(50), nullable=False, comment='课程名称')
    override_course_type = Column(Integer, nullable=True,
                                  comment='value used to override course_type '
                                          'defined in course, e.g. in a 1V4 '
                                          'course, the teacher want to teach '
                                          'one of his student due to the '
                                          'student resorting to help.')
    progress = Column(String(255), nullable=True,
                      comment='after finish this class, the progress desc of '
                              'this course')
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_schedules = db.relationship('Course', backref='course_schedules',
                                       lazy=True)


class CoursewareCheckResultEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    BEFORE_CHECK:待审核
    CHECK_PASSED：审核通过
    CHECK_DENY：审核驳回
    PREVIEW：可以预览
    NO_PREVIEW：不可以预览
    """
    BEFORE_CHECK = 1
    CHECK_PASSED = 2
    CHECK_DENY = 3
    PREVIEW = 4
    NO_PREVIEW = 5


class CourseStatueEnum(enum.IntEnum):
    """
    EFFECTIVE:有效
    INVALID:无效
    """
    EFFECTIVE = 98
    INVALID = 99

class CourseScheduleStatueEnum(enum.IntEnum):
    """
    CLASS_BEGIN:已经上课
    NO_CLASS:未上课
    CANCEL:取消
    TROUBLE_CLASS:问题课程
    """

    NO_CLASS = 1
    CLASS_BEGIN = 2
    CANCEL =  3
    TROUBLE_CLASS = 4

class CourseClassTypeEnum(enum.IntEnum):
    """
    1:1V1
    2:1V2
    3:1V3
    4:1V4
    5:1V6
    6:1V10
    7:1V15
    8:1V20
    """
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 6
    V6 = 10
    V7 = 15
    V8 = 20

class Courseware(EntityMixin, db.Model):
    """
    PPT or something showing in course uploaded by teacher
    before course study, needs to be checked by admin
    """
    ware_desc = Column(String(2000), nullable=False, comment='课件描述')
    ware_name = Column(String(100), nullable=False, comment='课件名称')
    ware_url = Column(String(255), nullable=True, comment='课件存储地址')
    ware_uid = Column(String(120), nullable=True, index=True,
                      comment='e.g. duobei use')
    room_id = Column(String(2000), nullable=True, comment='classroom list')
    other_desc = Column(String(2000), nullable=True, comment="e.g. duobei use")
    checked_result = Column(Enum(CoursewareCheckResultEnum), nullable=True,
                            comment='admin check result',
                            server_default=CoursewareCheckResultEnum.
                            BEFORE_CHECK.name)
    is_view = Column(String(20), nullable=False,comment='是否允许查看',server_default='YES')
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_wares = db.relationship('Course', backref='course_wares',
                                   lazy=True)
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=True)


class ClassroomStateEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    """
    CREATED = 1
    DELETED = 2
    IN_USE = 3
    USED = 4


class ClassroomTypeEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    """
    ONE_VS_ONE = 1
    ONE_VS_MANY = 2
    PRIVATE_CLASS = 3
    PUBLIC_CLASS = 4


class CourseClassroom(EntityMixin, db.Model):
    provider = Column(Integer, nullable=False, comment='1:duobei, 2:xxx')
    room_title = Column(String(255), nullable=False)
    video_ready = Column(Integer, nullable=False, comment='0:disable, 1:enable')
    room_url = Column(String(4000), nullable=True)
    room_id = Column(String(120), nullable=True, index=True,
                     comment='provider returned id after room created')
    room_type = Column(Enum(ClassroomTypeEnum), nullable=False,
                       server_default=ClassroomTypeEnum.ONE_VS_ONE.name)
    room_uid = Column(String(255), nullable=True,
                      comment='room uuid')
    host_code = Column(String(255), nullable=True,
                       comment='store duobei host_code used as invite code')
    state = Column(Enum(ClassroomStateEnum), nullable=False,
                   server_default=ClassroomStateEnum.CREATED.name)
    duration_start = Column(DateTime, nullable=True)
    duration_end = Column(DateTime, nullable=True)
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=False)
    class_rooms = db.relationship('CourseSchedule', backref='class_rooms',
                                  lazy=True)


class ClassroomRoleEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    1：听众，2:老师，3：学生，4：兼课，5：助教
    """
    AUDIENCE = 1
    TEACHER = 2
    STUDENT = 3
    SIT_IN = 4
    ASSISTANT = 5


class ClassroomDeviceEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    """
    PC = 1
    PHONE = 2

class CourseClassParticipant(EntityMixin, db.Model):
    role_in_course = Column(Enum(ClassroomRoleEnum), nullable=False,
                            server_default=ClassroomRoleEnum.ASSISTANT.name)
    role_id = Column(String(255), nullable=True)
    role_uid = Column(String(255), nullable=True)
    access_url = Column(String(255), nullable=True)
    device_type = Column(Enum(ClassroomDeviceEnum), nullable=False,
                         server_default=ClassroomDeviceEnum.PC.name)
    role_id = Column(String(255), nullable=True)
    role_table = Column(String(60), nullable=True)
    role_table_id = Column(Integer, nullable=True)
    role_username = Column(String(60), nullable=True)
    attend_start = Column(DateTime, nullable=True)
    attend_end = Column(DateTime, nullable=True)
    assessment = Column(String(2000), nullable=True)
    remark = Column(String(2000), nullable=True)
    course_classroom_id = Column(Integer, ForeignKey('course_classroom.id'),
                                 nullable=False)
    classroom_participants = db.relationship('CourseClassroom',
                                             backref='classroom_participants',
                                             lazy=True)


class CourseAppointment(EntityMixin, db.Model):
    open_time_start = Column(DateTime, nullable=False, comment='试听开始时间')
    open_time_end = Column(DateTime, nullable=False, comment='试听结束时间')
    teacher_id = Column(Integer, ForeignKey('teacher.id'),
                        nullable=True)
    appointments = db.relationship('Teacher',
                                   backref='course_appointments',
                                   lazy=True)


class CourdeTypeEnum(enum.IntEnum):
    """
    COMMON :公共课程
    ONLINE :在线课程
    TRYOUT :试讲
    """
    COMMON = 1
    ONLINE = 2
    TRYOUT = 3

