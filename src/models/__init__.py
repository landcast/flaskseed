from src.models.common_models import db, session_scope, row_dict, \
    EntityMixin,ActionEvent
from src.models.teacher_models import Teacher, Certificate, TeacherSubject,TeacherState, \
    Interview, InterviewState,TeacherTime,TeacherHistory
from src.models.student_models import Student, StudentAppraisal, StudentState, \
    StudentSubject, StudySchedule, StudyResult, CourseAppraisal,StudentRequirements,\
    StudyAppointment, Homework,StudentSubjectOptional, StudyScheduleStudyState
from src.models.admin_models import Enrollment, Channel, SysUser, \
    Attachment, SmsLog, Menu, Region, Notification, FeedBack, RoleDefinition, \
    SysUserRole, SysControl, SysUserStateEnum
from src.models.order_models import Order, PayLog, Account,OrderStateEnum
from src.models.course_models import Course, Subject, CourseExam,CourseStatueEnum, \
    CourseSchedule, Curriculum, CourseClassroom, CourseClassParticipant, \
    Courseware, SubjectCategory, CoursewareCheckResultEnum, \
    ClassroomStateEnum, ClassroomTypeEnum, ClassroomRoleEnum, \
    ClassroomDeviceEnum

user_source = {'Student': Student, 'Teacher': Teacher, 'SysUser': SysUser}
