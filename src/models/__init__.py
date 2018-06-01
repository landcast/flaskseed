from src.models.common_models import db, session_scope, row_dict, \
    EntityMixin
from src.models.teacher_models import Teacher, Certificate, TeacherSubject
from src.models.student_models import Student, StudentAppraisal, \
    StudentSubject, StudySchedule, StudyResult, CourseAppraisal, \
    StudyAppointment, Homework
from src.models.admin_models import Enrollment, Channel, SysUser, \
    Attachment, SmsLog, Menu, Region, Notification, FeedBack, RoleDefinition, \
    SysUserRole
from src.models.order_models import Order, PayLog, Account
from src.models.course_models import Course, Subject, CourseExam, \
    CourseSchedule, Curriculum, CourseClassroom, CourseClassParticipant, \
    Courseware, SubjectCategory, CourseAppointment

user_source = {'Student': Student, 'Teacher': Teacher, 'SysUser': SysUser}