#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
from src.models import db, session_scope
from src.services import do_query
import hashlib

order = Blueprint('order', __name__)


@order.route('/main_query', methods=['POST'])
def query():
    """
    swagger-doc: 'do order query'
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
        description: 'created_at start in sql format YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      created_at_end:
        description: 'created_at end in sql format YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      order_type:
        description: 'order type'
        type: 'string'
      order_state:
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
            classes_number:
              description: 'classes number in this order'
              type: 'integer'
            order_type:
              description: 'order type'
              type: 'integer'
            order_state:
              description: 'order state'
              type: 'integer'
            updated_by:
              description: 'order updated by'
              type: 'string'
            created_at:
              description: 'order created at'
              type: 'string'
            teacher_name:
              description: 'teacher name of order'
              type: 'string'
            student_name:
              description: 'student name of order'
              type: 'string'
            order_amount:
              description: 'order price amount'
              type: 'integer'
    """
    j = request.json
    return jsonify(do_query(j, generate_sql))


def generate_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select o.id, c.course_name, c.classes_number, o.order_type, o.state,
        o.updated_by, o.created_at, t.nickname, s.nickname, o.amount
    from `order` o, student s, teacher t, course c, subject su,
    subject_category sc, curriculum cr
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id and
        su.curriculum_id = cr.id and su.subject_category_id = sc.id
    ''']
    if 'course_id' in params.keys():
        sql.append(' and c.course_id = :course_id')
    if 'course_name' in params.keys():
        sql.append(' and c.course_name = :course_name')
    if 'order_type' in params.keys():
        sql.append(' and o.order_type = :order_type')
    if 'order_state' in params.keys():
        sql.append(' and o.order_state = :order_state')
    if 'updated_by' in params.keys():
        sql.append(' and o.updated_by = :updated_by')
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and :created_at_end')
    if 'category_1' in params.keys():
        sql.append(' and cr.full_name like :category_1')
    if 'category_2' in params.keys():
        sql.append(' and sc.subject_category like :category_2')
    if 'category_3' in params.keys():
        sql.append(' and su.subject_name like :category_3')
    # current_app.logger.debug(sql)
    return ['id', 'course_name', 'classes_number', 'order_type', 'order_state',
            'updated_by', 'created_at', 'teacher_name', 'student_name',
            'order_amount'], ''.join(sql)
