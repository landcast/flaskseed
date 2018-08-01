from flask import current_app
from src.models import db, session_scope, Student, Teacher, Course, CourseSchedule, ThirdDateLog, \
    StudySchedule, Courseware
from src.services import classin_service


def after_insert(table_name, table_id, session=None):
    current_app.logger.debug('listen start------------>' + table_name + '--------------' + str(table_id))
    if not session:
        session = db.session()
        need_commit = True
    else:
        need_commit = False

    current_app.logger.debug('need_commit------------>'+str(need_commit) )

    if 'student' == table_name:
        student = session.query(Student).filter_by(id=table_id).one_or_none()
        if student.mobile is not None:
            student_id = classin_service.register(student.mobile, student.nickname, student.password, 0, 'en')
            saveThirdDateLog(table_name, table_id, student_id, '')

    if 'teacher' == table_name:
        teacher = session.query(Teacher).filter_by(id=table_id).one_or_none()
        if teacher.mobile is not None:
            teacher_id = classin_service.register(teacher.mobile, teacher.nickname, teacher.password, 0, 'en')
            saveThirdDateLog(table_name, table_id, teacher_id, '')
    if 'course' == table_name:
        current_app.logger.debug('course------------>1' )
        course = session.query(Course).filter_by(id=table_id).one_or_none()
        current_app.logger.debug('course------------>2' )
        folderId = createFolder('', course.course_name, table_name, course.id, session)
        current_app.logger.debug('course------------>3' )
        course_id = classin_service.addCourse(course.course_name, 0, folderId, 0, 'en')
        current_app.logger.debug('course------------>4' )
        saveThirdDateLog(table_name, table_id, course_id, '')
        current_app.logger.debug('course------------>5' )

    if 'course_schedule' == table_name:
        courseSchedule = session.query(CourseSchedule).filter_by(id=table_id).one_or_none()
        course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()
        thirdDateLog = session.query(ThirdDateLog).filter_by(table_id=course.id, table_name='course').one_or_none()
        thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=course.id,
                                                                 table_name='folder_course').one_or_none()
        teacher = session.query(Teacher).filter_by(id=course.primary_teacher_id).one_or_none()

        folderId = createFolder(thirdDate_forder.third_id, course.course_name, table_name, courseSchedule.id, session)
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

    if need_commit:
        session.commit()


def after_update(table_name, table_id, session=None):
    if not session:
        session = db.session()
        need_commit = True
    else:
        need_commit = False

    if 'course' == table_name:
        course = session.query(Course).filter_by(id=table_id).one_or_none()
        thirdDate_course = session.query(ThirdDateLog).filter_by(table_id=course.id, table_name='course').one_or_none()
        if 'DELETED' == course.delete_flag:
            classin_service.delCourse(thirdDate_course.third_id,0,'en')
        else:
            classin_service.editCourse(course.course_name, '0',thirdDate_course.third_id, 0, 'en')
    if 'course_schedule' == table_name:
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

    if 'courseware' == table_name:
        courseware = session.query(Courseware).filter_by(id=table_id).one_or_none()
        thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=courseware.course_schedule_id,
                                                                 table_name='folder_course_schedule').one_or_none()
        if 'DELETED' == courseware.delete_flag:
            classin_service.delFile(thirdDate_forder.third_id,0,'en')


    if need_commit:
        session.commit()


def saveThirdDateLog(tableName, tableId, thirdId, thirdDate, session):

    current_app.logger.debug('course------------>17' )

    sql = 'INSERT INTO third_date_log (table_name,table_id,third_id,third_date,created_at,updated_at) VALUES ('+tableName+','+tableId+','+thirdId+','+thirdDate+',now(),now()'+')'

    session.execute()
    current_app.logger.debug('course------------>18'+sql )


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
