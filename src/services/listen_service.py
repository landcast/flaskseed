from flask import current_app
from src.models import db, session_scope,Student,Teacher,Course,CourseSchedule,ThirdDateLog,\
    StudySchedule,Courseware
from src.services import classin_service


def after_insert(table_name, table_id):

    current_app.logger.debug('listen start------------>'+table_name+'--------------'+str(table_id))
    with session_scope(db) as session:
        if 'student' == table_name:
            student = session.query(Student).filter_by(id=table_id).one_or_none()
            student_id = classin_service.register(student.mobile,student.nickname,student.password,0,'en')
            saveThirdDateLog(table_name,table_id,student_id,'')

        if 'teacher' == table_name:
            teacher = session.query(Teacher).filter_by(id=table_id).one_or_none()
            teacher_id = classin_service.register(teacher.mobile,teacher.nickname,teacher.password,0,'en')
            saveThirdDateLog(table_name,table_id,teacher_id,'')
        if 'course' == table_name:
            course = session.query(Course).filter_by(id=table_id).one_or_none()
            folderId = createFolder('',course.course_name,table_name,course.id)
            course_id = classin_service.addCourse(course.course_name,0,folderId,'en')
            saveThirdDateLog(table_name,table_id,course_id,'')

        if 'course_schedule' == table_name:
            courseSchedule = session.query(CourseSchedule).filter_by(id=table_id).one_or_none()
            course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()
            thirdDateLog = session.query(ThirdDateLog).filter_by(table_id=course.id,table_name='course').one_or_none()
            thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=course.id,table_name='folder_course').one_or_none()
            teacher = session.query(Teacher).filter_by(id=course.primary_teacher_id).one_or_none()

            folderId = createFolder(thirdDate_forder.third_id,course.course_name,table_name,courseSchedule.id)
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

            class_id = classin_service.addOneCourseClass(thirdDateLog.third_id,courseSchedule.name,courseSchedule.start,courseSchedule.end,teacher.mobile,teacher.nickname,num,folderId,0,'en')
            saveThirdDateLog(table_name,table_id,class_id,'')
        if 'study_schedule' == table_name:
            studySchedule = session.query(StudySchedule).filter_by(id=table_id).one_or_none()
            courseSchedule = session.query(CourseSchedule).filter_by(id=studySchedule.course_schedule_id).one_or_none()
            student = session.query(Student).filter_by(id=studySchedule.student_id).one_or_none()
            thirdDateLog = session.query(ThirdDateLog).filter_by(table_id=courseSchedule.course_id,table_name='course').one_or_none()
            classin_service.addCourseStudent(thirdDateLog.third_id,1,student.mobile,student.nickname,0,'en')

        if 'courseware' == table_name:
            courseware = session.query(Courseware).filter_by(id=table_id).one_or_none()
            thirdDate_forder = session.query(ThirdDateLog).filter_by(table_id=courseware.course_schedule_id,table_name='folder_course_schedule').one_or_none()
            forderid = classin_service.createFolder(thirdDate_forder.third_id,courseware.ware_name)
            classin_service.uploadFile(forderid,courseware.ware_url,0,'en')


def after_update(table_name, table_id):
    with session_scope(db) as session:
        if 'student' == table_name:
            student = session.query(Student).filter_by(id=table_id).one_or_none()
            classin_service.register(student.mobile,student.nickname,student.password,0,'en')

        if 'teacher' == table_name:
            teacher = session.query(Teacher).filter_by(id=table_id).one_or_none()
            classin_service.register(teacher.mobile,teacher.nickname,teacher.password,0,'en')
        if 'course' == table_name:
            course = session.query(Course).filter_by(id=table_id).one_or_none()
            classin_service.editCourse(course.course_name,'0',0,'en')
        if 'course_schedule' == table_name:
            courseSchedule = session.query(CourseSchedule).filter_by(id=table_id).one_or_none()
            course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()
            thirdDate_course = session.query(ThirdDateLog).filter_by(table_id=course.id,table_name='course').one_or_none()
            thirdDate_class = session.query(ThirdDateLog).filter_by(table_id=courseSchedule.id,table_name='course_schedule').one_or_none()
            teacher = session.query(Teacher).filter_by(id=course.primary_teacher_id).one_or_none()

            classin_service.editCourseClass(thirdDate_course.third_id,thirdDate_class.third_id,courseSchedule.name,courseSchedule.start,courseSchedule.end,teacher.mobile,teacher.nickname,'0',0,'en')



def saveThirdDateLog(table_name,table_id,third_id,third_date):

    with session_scope(db) as session:
        homework = ThirdDateLog(table_name = table_name,
                                table_id = table_id,
                                third_id = third_id,
                                third_date = third_date.id,
                                delete_flag = 'IN_FORCE')
    session.add(homework)
    session.flush()


def createFolder(folderId,folderName,table_name,table_id):
    folderId = classin_service.createFolder(folderId,folderName)
    saveThirdDateLog('folder_'+table_name,table_id,folderId,'')
    return folderId


