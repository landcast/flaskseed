#!/usr/bin/env python
import time

from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *

from src.models import db, session_scope,Course,CourseSchedule,Order,StudySchedule,CourseClassroom,CourseExam,\
    StudyResult,StudyResultTypeEnum,Curriculum,SubjectCategory,Subject
from src.services import do_query, datetime_param_sql_format
from src.services import live_service

from src.models import  ClassroomTypeEnum

course = Blueprint('course', __name__)


@course.route('/package_query', methods=['POST'])
def query():
    """
    swagger-doc: 'do package query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      category_1:
        description: '一级分类'
        type: 'string'
      category_2:
        description: '二级分类'
        type: 'string'
      category_3:
        description: '三级分类'
        type: 'string'
      course_name:
        description: '课程名称'
        type: 'string'
      course_id:
        description: '课程id'
        type: 'string'
      updated_by:
        description: '更新操作人'
        type: 'string'
      created_at_start:
        description: '上课开始时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: '上课结束时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_type:
        description: '课程类型'
        type: 'string'
      course_state:
        description: '课程状态'
        type: 'string'
    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '课程id'
              type: 'integer'
            course_name:
              description: '课程英文名称'
              type: 'string'
            course_name_zh:
              description: '课程中文名称'
              type: 'string'
            course_type:
              description: '课程类型'
              type: 'integer'
            course_state:
              description: '课程状态'
              type: 'integer'
            updated_by:
              description: '最后更新人'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
    return jsonify(do_query(j, generate_sql))


def generate_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select c.`course_name`,c.`course_name_zh`,c.id,c.`course_type`,c.state,
    c.`updated_by`,c.`created_at`
    from   course c, subject su,subject_category sc, curriculum cr
    where  c.subject_id = su.id and
        su.curriculum_id = cr.id and su.subject_category_id = sc.id
    and c.state <> 99 and su.state <> 99 and sc.state <> 99 and cr.state <> 99    
    and c.`delete_flag` = 'IN_FORCE' and su.`delete_flag` = 'IN_FORCE' and su.`delete_flag` = 'IN_FORCE'  and cr.`delete_flag` = 'IN_FORCE' 
    ''']
    if 'course_id' in params.keys():
        sql.append(' and c.id = :course_id')
    if 'course_name' in params.keys():
        sql.append(" and (c.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or c.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'course_type' in params.keys():
        sql.append(' and c.course_type = :course_type')
    if 'order_state' in params.keys():
        sql.append(' and c.state = :course_state')
    if 'updated_by' in params.keys():
        sql.append(' and c.updated_by = :updated_by')
    if 'created_at' in params.keys():
        sql.append(
                ' and c.created_at between :created_at_start and '
                ':created_at_end')
    if 'category_1' in params.keys():
        sql.append(' and cr.id = :category_1')
    if 'category_2' in params.keys():
        sql.append(' and sc.id = :category_2')
    if 'category_3' in params.keys():
        sql.append(' and su.id = :category_3')

    sql.append(' order by c.id desc')

    return [ 'course_name', 'course_name_zh','id', 'course_type', 'state',
            'updated_by', 'created_at'], ''.join(sql)


@course.route('/category_query', methods=['POST'])
def category_query():
    """
    swagger-doc: 'do package query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_name:
        description: '课程名称'
        type: 'string'
      course_id:
        description: '课程id'
        type: 'string'
      updated_by:
        description: '更新人'
        type: 'string'
      created_at_start:
        description: '课程开始时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: '课程结束时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_state:
        description: '课程状态'
        type: 'string'
    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '课程id'
              type: 'integer'
            name:
              description: '课程中文名称'
              type: 'string'
            name_zh:
              description: '课程英文名车'
              type: 'string'
            level:
              description: '层级，1，2，3'
              type: 'integer'
            state:
              description: '课程状态'
              type: 'integer'
            updated_by:
              description: '更新人'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
    return jsonify(do_query(j, category_sql))


def category_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''

    sql = ['''
    select t.* from (select full_name as name,full_name_zh as name_zh,id,
    updated_by,created_at,state,1 'level' from `curriculum` cu where cu.state <> 99 and cu.`delete_flag` = 'IN_FORCE' 
    union all select subject_category as name,subject_category_zh as name_zh,
    id,updated_by,created_at,state,2 'level' from subject_category where state <> 99 and `delete_flag` = 'IN_FORCE'
    union all select subject_name as name,subject_name_zh as name_zh,id,
    updated_by,created_at,state,3 'level' from subject where  state <> 99 and `delete_flag` = 'IN_FORCE') t where 1=1
    ''']
    if 'course_id' in params.keys():
        sql.append(' and t.id = :course_id')
    if 'course_name' in params.keys():
        sql.append(" and (t.name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or t.name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'course_state' in params.keys():
        sql.append(' and t.state = :course_state')
    if 'updated_by' in params.keys():
        sql.append(' and t.updated_by = :updated_by')
    if 'created_at' in params.keys():
        sql.append(
                ' and t.created_at between :created_at_start and '
                ':created_at_end')
    sql.append(' order by t.id desc')
    current_app.logger.debug(sql)
    return ['name', 'name_zh', 'id', 'updated_by', 'created_at',
            'state', 'level'], ''.join(sql)


@course.route('/schedule', methods=['POST'])
def schedule():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_id:
        description: '课程id'
        type: 'string'
      class_at_start:
        description: '课程开始时间,用户选择时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      class_at_end:
        description: '课程结束时间，排课之后的最后一堂课结束时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      schedules:
        description: '课表数据，数组数据'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_id = request.json['course_id']
    schedules = request.json['schedules']

    with session_scope(db) as session:

        course = session.query(Course).filter_by(id=course_id).one_or_none()

        if course is None :
            return jsonify({
                "error": "not found course: {0}".format(
                    course_id)
            }), 500

        orders = session.query(Order).filter_by(course_id = course.id , state=98 , payment_state=2).all()

        if orders is None or len(orders) < 1:
            return jsonify({
                "error": "found order existing in {0}".format(
                    course_id)
            }), 500

        for index, item in enumerate(schedules):

            start = item['start'].replace('T', ' ').replace('Z', '')
            end = item['end'].replace('T', ' ').replace('Z', '')

            courseschedule = CourseSchedule(
                start = start,
                end = end,
                name = item['course_name'],
                state = 1,
                override_course_type=course.course_type,
                course_id = course_id,
                delete_flag = 'IN_FORCE',
                updated_by=getattr(g, current_app.config['CUR_USER'])['username']
            )
            session.add(courseschedule)
            session.flush()

            class_type =ClassroomTypeEnum.ONE_VS_ONE.name

            if course.class_type != 1:
                class_type = ClassroomTypeEnum.ONE_VS_MANY.name

            live_service.create_room(getattr(g, current_app.config['CUR_USER'])['username'], courseschedule.id,item['course_name'], getTimeDiff(start,end),class_type,item['start'],0,'en')

            if courseschedule is None:
                return jsonify({
                    "error": "courseschedule error"
                }), 500

            for order in orders:

                sudyschedule = StudySchedule(
                    actual_start = start,
                    actual_end = end,
                    name = item['course_name'],
                    study_state = 1,
                    order_id = order.id,
                    course_schedule_id = courseschedule.id,
                    student_id = order.student_id,
                    delete_flag = 'IN_FORCE',
                    updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                )

                session.add(sudyschedule)
                session.flush()
                setattr(order,'payment_state',8)
                session.add(order)
                session.flush()

        setattr(course,'start',request.json['class_at_start'].replace('T', ' ').replace('Z', ''))
        setattr(course,'end',request.json['class_at_end'].replace('T', ' ').replace('Z', ''))
        session.add(course)
        session.flush()

    return jsonify({'id':courseschedule.id })


@course.route('/schedule_compensate', methods=['POST'])
def schedule_compensate():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课程id'
        type: 'string'
      start:
        description: '课程开始时间 format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      end:
        description: '课程结束时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      schedule_type:
        description: '课节类型'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_schedule_id = request.json['course_schedule_id']
    start = request.json['start'].replace('T', ' ').replace('Z', '')
    end = request.json['end'].replace('T', ' ').replace('Z', '')
    schedule_type = request.json['schedule_type']

    with session_scope(db) as session:

        courseSchedule = session.query(CourseSchedule).filter_by(id=course_schedule_id).one_or_none()

        if courseSchedule is None:
            return jsonify({
                "error": "not found course_schedule: {0}".format(
                    course_schedule_id)
            }), 500


        courseschedule = CourseSchedule(
            start = start,
            end = end,
            name = courseSchedule.name,
            state = 98,
            override_course_type=courseSchedule.override_course_type,
            course_id = courseSchedule.course_id,
            schedule_type = schedule_type,
            delete_flag = 'IN_FORCE',
            updated_by=getattr(g, current_app.config['CUR_USER'])['username']
        )
        session.add(courseschedule)
        session.flush()

        course = session.query(Course).filter_by(id=courseSchedule.course_id).one_or_none()

        class_type =ClassroomTypeEnum.ONE_VS_ONE.name

        if course.class_type != 1:
            class_type = ClassroomTypeEnum.ONE_VS_MANY.name

        live_service.create_room(getattr(g, current_app.config['CUR_USER'])['username'], courseschedule.id,courseSchedule.name, getTimeDiff(start,end),class_type,request.json['start'],0,'en')

        studyschedules = session.query(StudySchedule).filter_by(course_schedule_id=course_schedule_id).all()

        for studyschedule in studyschedules:

            sudyschedule = StudySchedule(
                actual_start = start,
                actual_end = end,
                name = courseSchedule.name,
                study_state = 1,
                order_id = studyschedule.order_id,
                course_schedule_id = courseschedule.id,
                student_id = studyschedule.student_id,
                schedule_type = schedule_type,
                delete_flag = 'IN_FORCE',
                updated_by=getattr(g, current_app.config['CUR_USER'])['username']
            )

            session.add(sudyschedule)
            session.flush()


    return jsonify({'id':courseschedule.id })


@course.route('/edit_course_schedule', methods=['POST'])
def upload_courseware():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课节id'
        type: 'string'
      start:
        description: '开始时间'
        type: 'string'
      end:
        description: '结束时间'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_schedule_id = request.json['course_schedule_id']
    start = request.json['start'].replace('T', ' ').replace('Z', '')
    end = request.json['end'].replace('T', ' ').replace('Z', '')

    with session_scope(db) as session:

        courseSchedule = session.query(CourseSchedule).filter_by(id=course_schedule_id).one_or_none()

        courseclassroom = session.query(CourseClassroom).filter_by(course_schedule_id=course_schedule_id).one_or_none()

        if courseSchedule is None or courseclassroom is None:
            return jsonify({
                "error": "not found course_schedule: {0}".format(
                    course_schedule_id)
            }), 500

        setattr(courseSchedule,'start',start)
        setattr(courseSchedule,'end',end)
        session.add(courseSchedule)
        session.flush()

        live_service.edit_room(getattr(g, current_app.config['CUR_USER'])['username'],courseclassroom.room_id,courseclassroom.room_title,
                               getTimeDiff(start,end),request.json['start'],request.json['end'],0,'en')

        studyschedules = session.query(StudySchedule).filter_by(course_schedule_id=course_schedule_id).all()

        if studyschedules is None or len(studyschedules)<1:
            return jsonify({
                "error": "not found Course_Class_room: {0}".format(
                    course_schedule_id)
            }), 500

        for studyschedule in studyschedules:

            setattr(studyschedule,'actual_start',start)
            setattr(studyschedule,'actual_end',end)
            session.add(studyschedule)
            session.flush()

    return jsonify({'id':courseSchedule.id })


@course.route('/edit_course_schedule_type', methods=['POST'])
def edit_course_schedule_type():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课节id'
        type: 'string'
      type:
        description: '类型'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_schedule_id = request.json['course_schedule_id']
    type = request.json['type']

    with session_scope(db) as session:

        courseSchedule = session.query(CourseSchedule).filter_by(id=course_schedule_id).one_or_none()

        if courseSchedule is None :
            return jsonify({
                "error": "not found course_schedule: {0}".format(
                    course_schedule_id)
            }), 500

        setattr(courseSchedule,'schedule_type',type)
        session.add(courseSchedule)
        session.flush()

        studyschedules = session.query(StudySchedule).filter_by(course_schedule_id=course_schedule_id).all()

        if studyschedules is None or len(studyschedules)<1:
            return jsonify({
                "error": "not found Course_Class_room: {0}".format(
                    course_schedule_id)
            }), 500

        for studyschedule in studyschedules:

            setattr(studyschedule,'schedule_type',type)
            session.add(studyschedule)
            session.flush()

    return jsonify({'id':courseSchedule.id })

@course.route('/common', methods=['POST'])
def course_common():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: '教师名称'
        type: 'string'
      teacher_id:
        description: '教师id'
        type: 'string'
      course_name:
        description: '课包名称'
        type: 'string'
      student_name:
        description: '学生名称'
        type: 'string'
      class_at:
        description: '上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      state:
        description: '课程状态，1：带排课，2：上课中，3：已完成'
        type: 'string'
      courseware:
        description: '课件状态，0：未上传，1：已上传'
        type: 'string'
    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '课程id'
              type: 'integer'
            teacher_name:
              description: '教师账号'
              type: 'integer'
            course_name:
              description: '课包英文名称'
              type: 'string'
            course_name_zh:
              description: '课包中文名称'
              type: 'string'
            student_name:
              description: '学生账号'
              type: 'string'
            start:
              description: '开始时间,如果没有就是带排课'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            classes_number:
              description: '总课程数'
              type: 'string'
            finish:
              description: '已经上完的程数'
              type: 'string'
            course_schedule_id:
              description: '总排课数大于0就是已经排课，0未排课'
              type: 'string'
            courseware_num:
              description: '大于0就是已经上传，否则未上传'
              type: 'int'
    """
    j = request.json
    datetime_param_sql_format(j, ['class_at']),
    return jsonify(do_query(j, course_common_sql))


def course_common_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
        select * from (select c.id ,c.course_name,c.course_name_zh,concat(t.`first_name`,' ',t.`middle_name`,' ',t.`last_name`)  as teacher_name,
        (select GROUP_CONCAT(s.name) from student s,`order` o where s.id = o.student_id and o.`delete_flag` = 'IN_FORCE' and o.state <> 99 and o.`delete_flag` = 'IN_FORCE' 
        and o.course_id = c.id ) as student_name,
        c.start,c.end end,c.classes_number,(select count(*) from course_schedule where course_id = c.id and `delete_flag` = 'IN_FORCE' and end < now()) as finish,
        c.open_grade,(select id from `course_schedule` where course_id = c.id group by c.id) as course_schedule_id,
         
      (select count(*) from courseware cs where c.`id` = cs.`course_id` and cs.`delete_flag` = 'IN_FORCE') as courseware_num,t.id as teacher_id
         from 
        course c,
        teacher t where t.id = c.`primary_teacher_id` and c.`delete_flag` = 'IN_FORCE'and t.`delete_flag` = 'IN_FORCE' and c.`class_type` < 3 
        ) t where 1=1
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and t.teacher_name like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'teacher_id' in params.keys():
        sql.append(" and t.teacher_id=:teacher_id")

    if 'student_name' in params.keys():
        sql.append(" and t.student_name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'course_name' in params.keys():
        sql.append(" and (t.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or t.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` <:class_at and t.`end` >:class_at')
    if 'state' in params.keys() and '1' ==params['state'] :
        sql.append(' and t.course_schedule_id is null')

    if 'state' in params.keys() and '2' ==params['state'] :
        sql.append(' and t.finish <= t.classes_number')

    if 'state' in params.keys() and '3' ==params['state'] :
        sql.append(' and t.finish > t.classes_number')

    if 'courseware' in params.keys() and '0' ==params['courseware'] :
        sql.append(' and t.courseware_num = 0')

    if 'courseware' in params.keys() and '1' ==params['courseware'] :
        sql.append(' and t.courseware_num > 0')
    sql.append(' order by t.id desc')

    return ['id', 'course_name', 'course_name_zh', 'teacher_name', 'student_name',
            'start', 'end','classes_number','finish','course_schedule_id','open_grade','courseware_num'], ''.join(sql)


@course.route('/course_schedule', methods=['POST'])
def course_schedule():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_id:
        description: '课包id'
        type: 'string'
    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: 'course_schedule_id'
              type: 'integer'
            name:
              description: '课程名称'
              type: 'integer'
            start:
              description: '开始时间'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            courseware_num:
              description: '课件数量'
              type: 'string'
            schedule_type:
              description: '课程状态'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['class_at']),
    return jsonify(do_query(j, course_schedule_sql))


def course_schedule_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
        select cs.id,cs.`name`,cs.`start`,cs.`end`,(select count(*) from courseware where course_schedule_id = cs.id)  as courseware_num,cs.`schedule_type`
	    from course_schedule cs
        where  cs.`delete_flag` = 'IN_FORCE' 
    ''']
    sql.append(" and cs.course_id=:course_id")

    sql.append(' order by cs.id desc')
    return ['id', 'name', 'start', 'end', 'courseware_num','schedule_type'], ''.join(sql)


@course.route('/common_homework', methods=['POST'])
def homework():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_schedule_id:
        description: 'course_schedule_id 课节id'
        type: 'string'


    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '作业id'
              type: 'integer'
            question_name:
              description: '作业名称'
              type: 'string'
            question_text:
              description: '问题'
              type: 'string'
            question_attachment_url:
              description: '问题附件，可以是json'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            course_name:
              description: '课程名称'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, my_homework_sql))


def my_homework_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select hm.id,question_name,homework_type,question_text,question_attachment_url,answer_text,answer_attachment_url,score,score_remark,score_reason,hm.created_at,t.nickname as teacher_name,c.course_name,t.avatar as teacher_avatar
    from homework hm,study_schedule sc,course c,teacher t,course_schedule cs
    where 
    hm.study_schedule_id = sc.id and cs.course_id = c.id and c.`primary_teacher_id` = t.id and sc.course_schedule_id = cs.id and hm.homework_type = 1
    and c.state<> 99 
    and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and sc.`delete_flag` = 'IN_FORCE' and hm.`delete_flag` = 'IN_FORCE'  and cs.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and cs.id =:course_schedule_id')

    sql.append(' order by hm.id desc')

    current_app.logger.debug(sql)

    return ['id', 'question_name','question_text', 'question_attachment_url', 'created_at'], ''.join(sql)


@course.route('/common_summary', methods=['POST'])
def common_summary():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_schedule_id:
        description: 'course_schedule_id 课节id'
        type: 'string'


    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: 'study_schedule_id'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            teacher_evaluation:
              description: '教师评价'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, common_summary_sql))


def common_summary_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select ss.id as study_schedule_id,s.nickname as student_name,ss.teacher_evaluation
    from course_schedule cs,study_schedule ss,student s
    where cs.id = ss.`course_schedule_id` and ss.student_id = s.id
    and cs.`delete_flag` = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and cs.id =:course_schedule_id')

    sql.append(' order by cs.id desc')

    current_app.logger.debug(sql)

    return ['study_schedule_id', 'student_name','teacher_evaluation'], ''.join(sql)



@course.route('/common_summary_result', methods=['POST'])
def common_summary_result():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_id:
        description: '课程id'
        type: 'string'
      type:
        description: 'SUMMARY:总结ACHIEVEMENT：成绩单'
        type: 'string'

    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            study_result_id:
              description: 'study_result_id'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            created_at:
              description: '上传时间'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, common_summary_result_sql))


def common_summary_result_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select ss.id as study_result_id,s.nickname as student_name,ss.created_at
    from study_result ss,student s
    where  ss.student_id = s.id
    and ss.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and ss.course_id =:course_id')

    sql.append(' and ss.result_type =:type')

    sql.append(' order by ss.id desc')

    current_app.logger.debug(sql)

    return ['study_result_id', 'student_name','created_at'], ''.join(sql)


@course.route('/common_summary_add', methods=['POST'])
def common_summary_add():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_id :
        description: '课程id'
        type: 'string'
      student_id :
        description: '学生id'
        type: 'string'
      start :
        description: '开始时间'
        type: 'string'
      end :
        description: '结束时间'
        type: 'string'
      evaluation :
        description: '评价'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_id = request.json['course_id']
    student_id = request.json['student_id']
    start = request.json['start'].replace('T', ' ').replace('Z', '')
    end = request.json['end'].replace('T', ' ').replace('Z', '')
    evaluation = request.json['evaluation']

    with session_scope(db) as session:

        course = session.query(Course).filter_by(id=course_id).one_or_none()

        if course is None :
            return jsonify({
                "error": "not found course: {0}".format(
                    course_id)
            }), 500

        courseExam =CourseExam( course_id=course.id,
                                start= start,
                                end=end,
                                state =98,
                                exam_desc='evaluation',
                                delete_flag = 'IN_FORCE',
                                updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                        )
        session.add(courseExam)
        session.flush()
        studyResult =StudyResult( evaluation= evaluation,
                                  result_type= StudyResultTypeEnum.SUMMARY.name,
                                 student_id= student_id,
                                 course_id = course.id,
                                 course_exam_id = courseExam.id,
                                 delete_flag = 'IN_FORCE',
                                 updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                                )

        session.add(studyResult)
        session.flush()

    return jsonify({'id':studyResult.id })



@course.route('/common_evaluation', methods=['POST'])
def common_evaluation():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_schedule_id:
        description: '课程计划id'
        type: 'string'

    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '学生id'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            teacher_score:
              description: '老师的星级'
              type: 'string'
            student_score:
              description: '学生的星级'
              type: 'string'
            teacher_evaluation:
              description: '老师的评价'
              type: 'string'
            teacher_name:
              description: '老师名字'
              type: 'string'
            name:
              description: '课节名字'
              type: 'string'
            teacher_result:
              description: '学生给老师的的反馈'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, common_evaluation_sql))


def common_evaluation_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
            select 
            s.id,s.name as student_name,ss.teacher_score,student_score,teacher_evaluation,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,cs.name,ss.teacher_result
            from  course_schedule cs,study_schedule ss , student s,teacher t,course c
            where  cs.id = ss.course_schedule_id and ss.student_id = s.id and cs.course_id = c.id and c.primary_teacher_id = t.id
            and cs.delete_flag = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and cs.id =:course_schedule_id')

    sql.append(' order by cs.id desc')

    return ['id', 'student_name','teacher_score','student_score','teacher_evaluation','teacher_name','name','teacher_result'], ''.join(sql)


@course.route('/common_homework_student', methods=['POST'])
def common_homework_student():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_schedule_id:
        description: 'course_schedule_id 课节id'
        type: 'string'
      homework_id:
        description: '作业id'
        type: 'string'


    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            id:
              description: '作业id'
              type: 'integer'
            title:
              description: '作业名称'
              type: 'string'
            answer_text:
              description: '答案描述'
              type: 'string'
            answer_attachment_url:
              description: '答案附件'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            student_name:
              description: ''
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, common_homework_student_sql))


def common_homework_student_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select hm.id,hm.question_name as title,hm.answer_text,hm.created_at,hm.answer_attachment_url,s.name as student_name
    from homework hm,study_schedule sc,student s
    where 
    hm.study_schedule_id = sc.id and sc.student_id = s.id and hm.homework_type = 2 
    and s.`delete_flag` = 'IN_FORCE'  and sc.`delete_flag` = 'IN_FORCE' and hm.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and sc.course_schedule_id =:course_schedule_id')

    sql.append(' and hm.homework_id =:homework_id')

    sql.append(' order by hm.id desc')

    current_app.logger.debug(sql)

    return ['id', 'title','answer_text', 'created_at','answer_attachment_url','student_name'], ''.join(sql)



@course.route('/member', methods=['POST'])
def member():
    """
    swagger-doc: 'do my homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_id:
        description: '课程id'
        type: 'string'

    res:
      num_results:
        description: 'objects returned by query in current page'
        type: 'integer'
      page:
        description: 'current page no in total pages'
        type: 'integer'
      total_pages:
        description: 'total pages'
        type: 'integer'
      objects:
        description: 'objects returned by query'
        type: array
        items:
          type: object
          properties:
            teacher_name:
              description: '教师名称'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            assist_teacher_name:
              description: '助教名称呢'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, member_sql))


def member_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
        select concat(t.`first_name`,' ',t.`middle_name`,' ',t.`last_name`)  as teacher_name,c.course_name,c.course_name_zh,
        (select GROUP_CONCAT(s.name) from `order` o,student s  where o.student_id = s.id  and o.`delete_flag` = 'IN_FORCE' and o.course_id = c.id and s.state <> 99 and s.`delete_flag` = 'IN_FORCE') as student_name,
        (select concat(`first_name`,' ',`middle_name`,' ',`last_name`)  from teacher where id = c.`assist_teacher_id`) as assist_teacher_name
         from 
        course c left join course_schedule cs on c.id = cs.course_id and cs.`delete_flag` = 'IN_FORCE',
        teacher t where t.id = c.`primary_teacher_id` and c.`delete_flag` = 'IN_FORCE'and t.`delete_flag` = 'IN_FORCE' 
    ''']

    sql.append(' and c.id =:course_id')

    sql.append(' order by c.id desc')

    return ['teacher_name','course_name','course_name_zh','student_name','assist_teacher_name'], ''.join(sql)


@course.route('/del_course_package', methods=['POST'])
def del_course_package():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_id:
        description: '课程id'
        type: 'string'
      type:
        description: '1:一级，2：二级，3：三级，4：课包'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_id = request.json['course_id']
    type = request.json['type']

    with session_scope(db) as session:


        if type == '1':
            curriculum = session.query(Curriculum).filter_by(id=course_id).one_or_none()

            if curriculum is None :
                return jsonify({
                    "error": "not found curriculum: {0}".format(
                        course_id)
                }), 500


            subjectCategory = session.query(SubjectCategory).filter_by(curriculum_id=curriculum.id).all()

            if  len(subjectCategory)>0:
                return jsonify({
                    "error": "found subjectCategory: {0} not delete".format(
                        course_id)
                }), 500

            setattr(curriculum,'delete_flag','DELETED')
            session.add(curriculum)
            session.flush()

        if type == '2':
            subjectCategory = session.query(SubjectCategory).filter_by(id=course_id).one_or_none()

            if subjectCategory is None :
                return jsonify({
                    "error": "not found subjectCategory: {0}".format(
                        course_id)
                }), 500


            subjects = session.query(Subject).filter_by(subject_category_id=subjectCategory.id).all()

            if len(subjects)>0:
                return jsonify({
                    "error": "found subjects: {0} not delete".format(
                        course_id)
                }), 500

            setattr(subjectCategory,'delete_flag','DELETED')
            session.add(subjectCategory)
            session.flush()

        if type == '3':
            subject = session.query(Subject).filter_by(id=course_id).one_or_none()

            if subject is None :
                return jsonify({
                    "error": "not found subject: {0}".format(
                        course_id)
                }), 500


            course = session.query(Course).filter_by(subject_id=subject.id).all()

            if len(course)>0:
                return jsonify({
                    "error": "found subjects: {0} not delete".format(
                        course_id)
                }), 500

            setattr(subject,'delete_flag','DELETED')
            session.add(subject)
            session.flush()

        if type == '4':
            course = session.query(Course).filter_by(id=course_id).one_or_none()

            if course is None :
                return jsonify({
                    "error": "not found course: {0}".format(
                        course_id)
                }), 500


            orders = session.query(Order).filter_by(course_id=course.id).all()

            if len(orders)>0:
                return jsonify({
                    "error": "found course: {0} not delete".format(
                        course_id)
                }), 500

            setattr(course,'delete_flag','DELETED')
            session.add(course)
            session.flush()

    return jsonify({'id':course_id })


@course.route('/add_student_schedule', methods=['POST'])
def add_student_schedule():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_id:
        description: '课程id'
        type: 'string'
      student_id:
        description: '学生id'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_id = request.json['course_id']
    student_id = request.json['student_id']

    with session_scope(db) as session:

        course = session.query(Course).filter_by(id=course_id).one_or_none()

        if course is None :
            return jsonify({
                "error": "not found course: {0}".format(
                    course_id)
            }), 500

        order = session.query(Order).filter_by(course_id = course.id,student_id = student_id, state=98 , payment_state=2).one_or_none()

        if order is None :
            return jsonify({
                "error": "found order existing in {0}".format(
                    course_id)
            }), 500

        csourseSchedules = session.query(CourseSchedule).filter_by(course_id = course.id).all()

        if csourseSchedules is None or len(csourseSchedules) < 1:
            return jsonify({
                "error": "not found CourseSchedule in {0}".format(
                    course_id)
            }), 500



        for csourseSchedule in csourseSchedules:

                sudyschedule = StudySchedule(
                    actual_start = csourseSchedule.start,
                    actual_end = csourseSchedule.end,
                    name = csourseSchedule.name,
                    study_state = 1,
                    order_id = order.id,
                    course_schedule_id = csourseSchedule.id,
                    student_id = order.student_id,
                    delete_flag = 'IN_FORCE',
                    updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                )

                session.add(sudyschedule)
                session.flush()
                setattr(order,'payment_state',8)
                session.add(order)
                session.flush()



    return jsonify({'id':course.id })






def getTimeDiff(timeStra,timeStrb):
    if timeStra>=timeStrb:
        return 0

    current_app.logger.debug('timeStrb-------->'+timeStrb)

    if "." in timeStra:
        timeStra = timeStra.split('.')[0]
        timeStrb = timeStrb.split('.')[0]

    ta = time.strptime(timeStra, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(timeStrb, "%Y-%m-%d %H:%M:%S")
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)

    secondsDiff=(dataTimeb-dataTimea).seconds
    #两者相加得转换成分钟的时间差
    minutesDiff=round(secondsDiff/60)

    current_app.logger.debug('minutesDiff-------->'+str(minutesDiff))
    return minutesDiff