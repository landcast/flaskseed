from sqlalchemy import event
from src.models.common_models import EntityMixin, db
from flask import current_app
from src.services import listen_service
from src.services import classin_service
from src.models import db, session_scope, Student, Teacher, Course, CourseSchedule, ThirdDateLog, \
    StudySchedule, Courseware
from datetime import datetime




# standard decorator style
@event.listens_for(EntityMixin, 'after_insert', propagate=True)
def receive_after_insert(mapper, connection, target):
    print('after_insert-1', target.__tablename__, target.id)
    current_app.logger.debug('after_insert---1--------->'+target.__tablename__+'--------------'+str(target.id))

    session = db.session()
    current_app.logger.debug('after_insert----2-------->')
    #listen_service.after_insert(target.__tablename__, target.id, session,connection)

    table_name = target.__tablename__
    table_id = target.id

    if 'course' == table_name:
        course = session.query(Course).filter_by(id=table_id).one_or_none()
        folderId = createFolder('', course.course_name, table_name, course.id, session)
        course_id = classin_service.addCourse(course.course_name, 0, folderId, 0, 'en')
        saveThirdDateLog(table_name, table_id, course_id, '',connection)

    if 'course_schedule' == table_name:
        courseSchedule = session.query(CourseSchedule).filter_by(id=table_id).one_or_none()
        course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()
        thirdDateLog = session.query(ThirdDateLog).filter_by(table_id=course.id, table_name='course').one_or_none()
        thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=course.id,
                                                                 table_name='folder_course').one_or_none()
        teacher = session.query(Teacher).filter_by(id=course.primary_teacher_id).one_or_none()

        folderId = createFolder(thirdDate_forder.third_id, courseSchedule.name, table_name, courseSchedule.id, session)
        num = 0
        if course.class_type == 3:
            num = 3
        elif course.class_type == 4:
            num = 4
        elif course.class_type == 5:
            num = 6
        elif course.class_type == 6:
            num = 10
        else:
            num = 2

        class_id = classin_service.addOneCourseClass(thirdDateLog.third_id, courseSchedule.name, courseSchedule.start,
                                                     courseSchedule.end, teacher.mobile, teacher.nickname, num,
                                                     folderId, 0, 'en')
        saveThirdDateLog(table_name, table_id, class_id, '', session)
    if 'study_schedule' == table_name:
        studySchedule = session.query(StudySchedule).filter_by(id=table_id).one_or_none()
        courseSchedule = session.query(CourseSchedule).filter_by(id=studySchedule.course_schedule_id).one_or_none()
        student = session.query(Student).filter_by(id=studySchedule.student_id).one_or_none()
        thirdDateLog = session.query(ThirdDateLog).filter_by(table_id=courseSchedule.course_id,
                                                             table_name='course').one_or_none()
        classin_service.addCourseStudent(thirdDateLog.third_id, 1, student.mobile, student.nickname, 0, 'en')

    if 'courseware' == table_name:
        courseware = session.query(Courseware).filter_by(id=table_id).one_or_none()
        thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=courseware.course_schedule_id,
                                                                 table_name='folder_course_schedule').one_or_none()
        forderid = classin_service.createFolder(thirdDate_forder.third_id, courseware.ware_name)
        classin_service.uploadFile(forderid, courseware.ware_url, 0, 'en')


# standard decorator style
@event.listens_for(EntityMixin, 'after_update', propagate=True)
def receive_after_update(mapper, connection, target):
    print('after_insert-1', target.__tablename__, target.id)
    current_app.logger.debug('vafter_update------------>'+target.__tablename__+'--------------'+str(target.id))

    session = db.session()
    listen_service.after_update(target.__tablename__, target.id,session)


def saveThirdDateLog(tableName, tableId, thirdId, thirdDate,connection):

    current_app.logger.debug('course------------>27' )
    connection.execute(
        "insert into third_date_log(table_name,table_id, "
        "third_id,third_date,created_at,updated_at) "
        "values('{}', '{}', '{}', '{}', '{}', '{}')".format(
            tableName, tableId, thirdId,
            thirdDate, datetime.now(), datetime.now()))
    current_app.logger.debug('course------------>28' )



def createFolder(folderId, folderName, table_name, table_id, session=None):
    if not session:
        session = db.session()
        need_commit = True
    else:
        need_commit = False
    folderId = classin_service.createFolder(folderId, folderName+str(table_id))
    saveThirdDateLog('folder_' + table_name, table_id, folderId, '', session)
    if need_commit:
        session.commit()
    return folderId



