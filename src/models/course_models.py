from src.models.common_models import db, EntityMixin
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class Curriculum(EntityMixin, db.Model):
    full_name = Column(String(120), nullable=False)
    desc = Column(String(255), nullable=True)
    prerequisite = Column(String(255), nullable=True)
    language_requirement = Column(String(255), nullable=True)


class SubjectCategory(EntityMixin, db.Model):
    subject_category = Column(String(120), nullable=False)


class Subject(EntityMixin, db.Model):
    subject_open_grade = Column(String(120), nullable=False)
    subject_name = Column(String(120), nullable=False)
    subject_desc = Column(String(120), nullable=True)
    subject_requirements = Column(String(120), nullable=True)
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
    course_name = Column(String(120), nullable=False)
    course_type = Column(Integer, nullable=False,
                         comment='enum, e.g. 1 v 1, 1 v 4, 1 v n')
    open_grade = Column(String(120), nullable=False)
    course_desc = Column(String(120), nullable=True)
    difficult_level = Column(Integer, nullable=True)
    critical_level = Column(Integer, nullable=True)
    course_requirements = Column(String(120), nullable=True)
    state = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
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
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False)
    exam_form = Column(String(255), nullable=True)
    exam_desc = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_schedules = db.relationship('Course', backref='course_exams',
                                       lazy=True)


class CourseSchedule(EntityMixin, db.Model):
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False)
    progress = Column(String(255), nullable=True,
                      comment='after finish this class, the progress desc of '
                              'this course')
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course_schedules = db.relationship('Course', backref='course_schedules',
                                       lazy=True)


class Courseware(EntityMixin, db.Model):
    '''
    PPT or something showing in course uploaded by teacher
    before course study, needs to be checked by admin
    '''
    ware_desc = Column(String(2000), nullable=False)
    ware_url = Column(String(255), nullable=True)
    other_desc = Column(String(2000), nullable=False, comment="e.g. duobei use")
    checked_result = Column(Integer, nullable=True,
                            comment='admin check result')
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=False)
    course_wares = db.relationship('CourseSchedule', backref='course_wares',
                                   lazy=True)


class CourseClassroom(EntityMixin, db.Model):
    provider = Column(Integer, nullable=False, comment='1:duobei, 2:xxx')
    room_title = Column(String(255), nullable=False)
    video_ready = Column(Integer, nullable=False, comment='0:disable, 1:enable')
    room_url = Column(String(255), nullable=False)
    room_id = Column(String(255), nullable=True)
    room_uid = Column(String(255), nullable=True,
                      comment='store duobei host_code')
    state = Column(Integer, nullable=False)
    duration_start = Column(DateTime, nullable=True)
    duration_end = Column(DateTime, nullable=True)
    course_schedule_id = Column(Integer, ForeignKey('course_schedule.id'),
                                nullable=False)
    class_rooms = db.relationship('CourseSchedule', backref='class_rooms',
                                  lazy=True)


class CourseClassParticipant(EntityMixin, db.Model):
    role_in_course = Column(Integer, nullable=False)
    role_id = Column(String(255), nullable=False)
    role_uid = Column(String(255), nullable=False)
    role_table = Column(String(60), nullable=False)
    role_table_id = Column(Integer, nullable=False)
    role_username = Column(String(60), nullable=False)
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
    open_time_start = Column(DateTime, nullable=False)
    open_time_end = Column(DateTime, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'),
                        nullable=False)
    appointments = db.relationship('Teacher',
                                   backref='course_appointments',
                                   lazy=True)
