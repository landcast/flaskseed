#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
from src.models import db, session_scope,Course,CourseSchedule,Order,StudySchedule
from src.services import do_query, datetime_param_sql_format
import hashlib

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
        description: 'course name'
        type: 'string'
      course_id:
        description: 'course id'
        type: 'string'
      updated_by:
        description: 'updated by'
        type: 'string'
      created_at_start:
        description: 'created_at start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: 'created_at end in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_type:
        description: 'order type'
        type: 'string'
      course_state:
        description: 'order state'
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
              description: 'course id'
              type: 'integer'
            course_name:
              description: 'course name'
              type: 'string'
            course_name_zh:
              description: 'course name zh'
              type: 'string'
            course_type:
              description: 'order type'
              type: 'integer'
            course_state:
              description: 'order state'
              type: 'integer'
            updated_by:
              description: 'order updated by'
              type: 'string'
            created_at:
              description: 'order created at'
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
        sql.append(' and c.course_id = :course_id')
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
        sql.append(" and cr.full_name like '%")
        sql.append(params['category_1'])
        sql.append("%'")
    if 'category_2' in params.keys():
        sql.append(" and sc.subject_category like '%")
        sql.append(params['category_2'])
        sql.append("%'")
    if 'category_3' in params.keys():
        sql.append(" and su.subject_name  like '%")
        sql.append(params['category_3'])
        sql.append("%'")
    return ['id', 'course_name', 'course_name_zh', 'course_type', 'state',
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
        description: 'course name'
        type: 'string'
      course_id:
        description: 'course id'
        type: 'string'
      updated_by:
        description: 'updated by'
        type: 'string'
      created_at_start:
        description: 'created_at start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: 'created_at end in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_state:
        description: 'order state'
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
              description: 'course id'
              type: 'integer'
            name:
              description: 'course name'
              type: 'string'
            name_zh:
              description: 'course name zh'
              type: 'string'
            level:
              description: '层级，1，2，3'
              type: 'integer'
            state:
              description: 'course state'
              type: 'integer'
            updated_by:
              description: 'order updated by'
              type: 'string'
            created_at:
              description: 'order created at'
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
    current_app.logger.debug(params)
    sql = ['''
    select t.* from (select full_name as name,full_name_zh as name_zh,id,
    updated_by,created_at,state,1 'level' from `curriculum` cu where cu.state <> 99 and cu.`delete_flag` = 'IN_FORCE' 
    union all select subject_category as name,subject_category_zh as name_zh,
    id,updated_by,created_at,state,2 'level' from subject_category where state <> 99 and `delete_flag` = 'IN_FORCE'
    union all select subject_name as name,subject_name_zh as name_zh,id,
    updated_by,created_at,state,3 'level' from subject where  state <> 99 and `delete_flag` = 'IN_FORCE') t
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
      schedules:
        description: '课表数据'
        type: 'string'
    res:
      verify_code:
        description: 'id'
        type: 'string'
    """
    course_id = request.json['course_id']
    schedules = request.json['schedules']

    with session_scope(db) as session:

        course = session.query(Course).filter_by(id=course_id).one_or_none()

        if course is None:
            return jsonify({
                "error": "not found course: {1}".format(
                    course_id)
            }), 500

        for order in session.query(Order).filter_by(course_id=course.id):

            for index, item in enumerate(schedules):

                courseschedule_id = 0

                if index == 0:
                    courseschedule = CourseSchedule(
                        start = item['start'].replace('T', ' ').replace('Z', ''),
                        end = item['end'].replace('T', ' ').replace('Z', ''),
                        state = 1,
                        override_course_type=course.course_type,
                        course_id = course_id,
                        delete_flag = 'IN_FORCE',
                        updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                    )
                    session.add(courseschedule)
                    session.flush()

                    courseschedule_id = courseschedule.id

                if courseschedule_id ==0 :
                    return jsonify({
                        "error": "courseschedule error"
                    }), 500

                sudyschedule = StudySchedule(
                    actual_start = item['start'].replace('T', ' ').replace('Z', ''),
                    actual_end = item['end'].replace('T', ' ').replace('Z', ''),
                    name = item['course_name'],
                    study_state = 1,
                    order_id = order.id,
                    course_schedule_id = courseschedule_id,
                    student_id = order.student_id,
                    delete_flag = 'IN_FORCE',
                    updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                )
                session.add(sudyschedule)
                session.flush()
