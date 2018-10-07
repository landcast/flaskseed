from flask import current_app
from datetime import datetime
from src.models import db, session_scope, Student, Teacher, Course, CourseSchedule, ThirdDateLog, \
    StudySchedule, Courseware,Interview
from src.services import classin_service,email_service



def after_update(table_name, table_id, session=None):
    if not session:
        session = db.session()
        need_commit = True
    else:
        need_commit = False

    if 'course12' == table_name:
        course = session.query(Course).filter_by(id=table_id).one_or_none()
        thirdDate_course = session.query(ThirdDateLog).filter_by(table_id=course.id, table_name='course').one_or_none()
        if 'DELETED' == course.delete_flag:
            classin_service.delCourse(thirdDate_course.third_id,0,'en')
        else:
            classin_service.editCourse(course.course_name, '0',thirdDate_course.third_id, 0, 'en')
    if 'course_schedule12' == table_name:
        courseSchedule = session.query(CourseSchedule).filter_by(id=table_id).one_or_none()
        thirdDate_class = session.query(ThirdDateLog).filter_by(table_id=courseSchedule.id,
                                                                table_name='course_schedule').one_or_none()
        thirdDate_course = session.query(ThirdDateLog).filter_by(table_id=course.id, table_name='course').one_or_none()

        if 'DELETED' == courseSchedule.delete_flag:
            classin_service.delCourseClass(thirdDate_course.third_id,thirdDate_class.third_id,0,'en')
        else:
            course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()

            teacher = session.query(Teacher).filter_by(id=course.primary_teacher_id).one_or_none()

            classin_service.editCourseClass(thirdDate_course.third_id, thirdDate_class.third_id, courseSchedule.name,
                                        courseSchedule.start, courseSchedule.end, teacher.mobile, teacher.nickname, '0', 0, 'en')

    if 'courseware12' == table_name:
        courseware = session.query(Courseware).filter_by(id=table_id).one_or_none()
        thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=courseware.course_schedule_id,
                                                                 table_name='folder_course_schedule').one_or_none()
        if 'DELETED' == courseware.delete_flag:
            classin_service.delFile(thirdDate_forder.third_id,0,'en')

    if 'interview' == table_name:
        interview = session.query(Interview).filter_by(id=table_id).one_or_none()
        teacher = session.query(Teacher).filter_by(id=interview.teacher_id).one_or_none()
        if interview.state == 6:
            email_service.sendEmail(teacher.email,teacher.first_name,'interview','interview1',1,'en')
        if interview.state == 9:
            email_service.sendEmail(teacher.email,teacher.first_name,'interview','interview7_T',1,'en')
        if interview.state == 10:
            email_service.sendEmail(teacher.email,teacher.first_name,'interview','interview7_F',1,'en')

    if 'teacher' == table_name:
        teacher = session.query(Teacher).filter_by(id=table_id).one_or_none()
        if teacher.state == 'CONTRACTOR':
            email_service.sendEmail(teacher.email,teacher.first_name,'training manual','study',1,'en')



    if need_commit:
        session.commit()


def saveThirdDateLog(tableName, tableId, thirdId, thirdDate,connection):

    current_app.logger.debug('course------------>17' )
    connection.execute(
        "insert into third_date_log(table_name,table_id, "
        "third_id,third_date,created_at,updated_at) "
        "values({}, '{}', '{}', '{}', '{}', '{}')".format(
            tableName, tableId, thirdId,
            thirdDate, datetime.now(), datetime.now()))
    current_app.logger.debug('course------------>18' )



def createFolder(folderId, folderName, table_name, table_id, session=None):
    if not session:
        session = db.session()
        need_commit = True
    else:
        need_commit = False
    folderId = classin_service.createFolder(folderId, folderName)
    saveThirdDateLog('folder_' + table_name, table_id, folderId, '', session)
    if need_commit:
        session.commit()
    return folderId
