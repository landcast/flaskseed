#!/usr/bin/env python
from filecmp import cmp

from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
from src.models import db, session_scope
from src.services import do_query
import hashlib
from src.services import do_query, datetime_param_sql_format
import json

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
    select c.id,c.`course_name`,(select count(*) from study_schedule where 
    student_id = s.id and study_state = 1) as finish,
		c.classes_number,
		t.`nickname`,
		cs.start,cs.end
    from `order` o, student s, teacher t, course c,`course_schedule`cs 
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.`id` = cs.course_id
        and o.`state` <> 99  and c.state<> 99 and cs.state <> 99
        and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE'    
    ''']
    sql.append("and s.id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_name' in params.keys():
        sql.append(
            ' and （c.course_name like :course_name or c.course_name_zh '
            'like:course_name)')
    if 'teacher_name' in params.keys():
        sql.append(' and t.nick_name like :teacher_name')
    if 'course_time' in params.keys():
        sql.append(
            ' and cs.start >:course_time and cs.end <:course_time')
    if 'course_status' in params.keys() \
            and params['course_status'] == '1':
        sql.append(' and cs.end >=:now()')
    if 'course_status' in params.keys() \
            and params['course_status'] == '2':
        sql.append(' and cs.end < now()')

    return ['id', 'course_name', 'finish', 'classes_number', 'nickname',
            'start', 'end'], ''.join(sql)


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
    datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
    return jsonify(do_query(j, my_order_sql))


def my_order_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select o.id,c.`course_name`,c.classes_number,o.`order_type`,
    o.`payment_state`,o.`created_at`,t.`nickname`,o.`amount`
    from `order` o, teacher t, course c
    where  o.course_id = c.id and
        c.primary_teacher_id = t.id
        and o.`state` <> 99 and c.state<> 99
        and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE'
    ''']

    sql.append(
        " and o.student_id =" + getattr(g, current_app.config['CUR_USER'])[
            'id'])

    if 'order_id' in params.keys():
        sql.append(' and o.id =:order_id')

    if 'course_name' in params.keys():
        sql.append(" and (c.course_name like '%").append(params['course_name']).append("%'");
        sql.append(" or c.course_name_zh like '%").append(params['course_name']).append("%')");

    if 'payment_state' in params.keys():
        sql.append(' and o.payment_state = :payment_state')
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and '
            ':created_at_end')

    return ['id', 'course_name', 'classes_number', 'order_type',
            'payment_state',
            'created_at', 'nickname', 'amount'], ''.join(sql)


@student.route('/my_homework', methods=['POST'])
def my_homework():
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
      study_schedule_id:
        description: 'study schedule id'
        type: 'string'
      homework_state:
        description: 'homework state 0:全部列表，1：我完成的，2：待完成的'
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
              description: 'homework id'
              type: 'integer'
            homework_type:
              description: 'homework type'
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
            answer_text:
              description: '答案'
              type: 'string'
            answer_attachment_url:
              description: '答案附件 可以是json'
              type: 'string'
            score:
              description: '得分'
              type: 'float'
            score_remark:
              description: '得分标记'
              type: 'string'
            score_reason:
              description: '得分原因'
              type: 'string'
            created_at:
              description: 'created at'
              type: 'string'
            teacher_name:
              description: 'teacher name'
              type: 'string'
            course_name:
              description: 'course name'
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
    select hm.id,question_name,homework_type,question_text,question_attachment_url,answer_text,answer_attachment_url,score,score_remark,score_reason,hm.created_at,t.nickname as teacher_name,c.course_name
    from homework hm,study_schedule sc,course c,teacher t,`order` o
    where 
    hm.study_schedule_id = sc.id and sc.order_id = o.id and o.course_id = c.id and c.`primary_teacher_id` = t.id
    and o.`state` <> 99  and c.state<> 99 
    and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and sc.`delete_flag` = 'IN_FORCE' and hm.`delete_flag` = 'IN_FORCE' 
    ''']
    sql.append(
        " and sc.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'study_schedule_id' in params.keys():
        sql.append(' and sc.id =:study_schedule_id')

    if 'homework_state' in params.keys() \
             and params['study_schedule_id']== '1':
        sql.append(' and study_schedule_id  in (select study_schedule_id '
                   'from homework he1,study_schedule sc1 '
                   'where homework_type = 2 and he1.`study_schedule_id` = sc1.id and sc1.`student_id` = )'
                   + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'homework_state' in params.keys() \
             and params['study_schedule_id'] == '2':
        sql.append(' and study_schedule_id  not in (select study_schedule_id '
                   'from homework he1,study_schedule sc1 '
                   'where homework_type = 2 and he1.`study_schedule_id` = sc1.id and sc1.`student_id` = )'
                   + getattr(g, current_app.config['CUR_USER'])['id'])

    return ['id', 'question_name', 'homework_type', 'question_text', 'question_attachment_url',
            'answer_text', 'answer_attachment_url', 'score', 'score_remark', 'score_reason', 'created_at',
            'teacher_name','course_name'], ''.join(sql)


