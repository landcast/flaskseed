#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
from src.models import db, session_scope
from src.services import do_query
import hashlib
from src.services import do_query, datetime_param_sql_format

student = Blueprint('student', __name__)


@student.route('/my_course', methods=['POST'])
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
      teacher_name:
        description: 'teacher name'
        type: 'string'
      course_time:
        description: 'course_time start in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
    select c.id,c.`course_name`,(select count(*) from study_schedule where student_id = s.id and study_state = 1) as finish,
		c.classes_number,
		t.`nickname`,
		cs.start,cs.end
    from `order` o, student s, teacher t, course c,`course_schedule`cs 
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.`id` = cs.course_id
    ''']
    sql.append("and o.studet_id ="+getattr(g, current_app.config['CUR_ID']))
    if 'course_name' in params.keys():
        sql.append(' and （c.course_name like :course_name or c.course_name_zh like:course_name)')
    if 'teacher_name'in params.keys():
        sql.append(' and t.nick_name like :teacher_name')
    if 'course_time'in params.keys():
        sql.append(
            ' and cs.start >:course_time and cs.end <:course_time')
    if 'course_status'in params.keys() \
            and 'course_status' == '1':
        sql.append(' and cs.end >=:now()')
    if 'course_status'in params.keys() \
            and 'course_status' == '2':
        sql.append(' and cs.end < now()')

    return ['id', 'course_name', 'course_name_zh', 'course_type', 'state',
            'updated_by', 'created_at'], ''.join(sql)

@student.route('/my_order', methods=['POST'])
def my_order():
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
      order_id:
        description: 'order id'
        type: 'string'
      payment_state:
        description: 'payment state'
        type: 'string'
      created_at_start:
        description: 'created_at start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: 'created_at end in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
            teacher_name:
              description: 'teacher name'
              type: 'string'
            classes_number:
              description: 'classes number'
              type: 'integer'
            order_type:
              description: 'order type'
              type: 'integer'
            payment_state:
              description: 'payment state'
              type: 'string'
            teacher_name:
              description: 'teacher_name'
              type: 'string'
            created_at:
              description: 'order created at'
              type: 'string'
            order_amount:
              description: 'order price amount'
              type: 'integer'
    """
    j = request.json
    datetime_param_sql_format(j, ['created_at_start','created_at_end']),
    return jsonify(do_query(j, my_order_sql))


def my_order_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select o.id,c.`course_name`,c.classes_number,o.`order_type`,o.`payment_state`,o.`created_at`,t.`nickname`,o.`amount`
    from `order` o, teacher t, course c
    where  o.course_id = c.id and
        c.primary_teacher_id = t.id
    ''']

    sql.append(" and o.studet_id ="+getattr(g, current_app.config['CUR_ID']))

    if 'order_id' in params.keys():
        sql.append(' and o.id =:order_id')

    if 'course_name' in params.keys():
        sql.append[' and （c.course_name like :course_name or c.course_name_zh like:course_name)']
    if 'payment_state'in params.keys():
        sql.append[' and o.payment_state = :payment_state']
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and :created_at_end')

    return ['id', 'course_name', 'course_name_zh', 'course_type', 'state',
            'updated_by', 'created_at'], ''.join(sql)
