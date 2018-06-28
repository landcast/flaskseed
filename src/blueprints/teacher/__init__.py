#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
from src.models import db, session_scope
from src.services import do_query
import hashlib
from src.services import do_query, datetime_param_sql_format

teacher = Blueprint('teacher', __name__)


@teacher.route('/my_course', methods=['POST'])
def my_course():
    """
    swagger-doc: 'do my course query'
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
      student_name:
        description: 'student name'
        type: 'string'
      course_time:
        description: 'created_at start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_status:
        description: 'course status 1：finish,2:go on'
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
            student_name:
              description: 'student name'
              type: 'string'
            finish:
              description: 'finish number'
              type: 'integer'
            classes_number:
              description: 'classes number'
              type: 'integer'
            start:
              description: 'course start'
              type: 'string'
            end:
              description: 'course end'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['course_time']),
    return jsonify(do_query(j, my_course_sql))


def my_course_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
     select c.id,c.`course_name`,(select count(*) from study_schedule where 
     student_id = s.id and study_state = 1) as finish,
		c.classes_number,
		s.`nickname` as student_name,
		cs.start,cs.end
    from `order` o, student s, teacher t, course c,`course_schedule`cs 
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.`id` = cs.course_id
        and o.`state` <> 99 and s.`state` <> 99 and c.state<> 99 and cs.state <> 99
        and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' 
    ''']
    sql.append(" and t.id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_name' in params.keys():
        sql.append(" and (c.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or c.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'student_name' in params.keys():
        sql.append(" and s.nickname like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'course_time' in params.keys():
        sql.append(
                ' and cs.start <:course_time and cs.end >:course_time')
    if 'course_status' in params.keys() \
            and params['course_status'] == '1':
        sql.append(' and cs.end >=:now()')
    if 'course_status' in params.keys() \
            and params['course_status'] == '2':
        sql.append(' and cs.end < now()')

    return ['id', 'course_name', 'course_name_zh', 'course_type', 'state',
            'updated_by', 'created_at'], ''.join(sql)
