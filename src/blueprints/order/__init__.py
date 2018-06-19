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
    required: ['username', 'password', 'usertype']
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
        description: 'created_at start'
        type: 'string'
      created_at_end:
        description: 'created_at end'
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
    select o.id, c.course_name, c.classes_number, o.order_type, o.state,
        o.updated_by, o.created_at, t.nickname, s.nickname, o.amount
    from `order` o, student s, teacher t, course c, subject su,
    subject_category sc, curriculum cr
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id and
        su.curriculum_id = cr.id and su.subject_category_id = sc.id
    :param params:
    :return:
    '''
    current_app.logger.debug(params['start'] + ', ' + params['end'])
    sql = 'select id, notice, updated_at from notification ' \
          'where updated_at between :start and :end order by updated_at ' \
          'desc'
    return ['seq', 'desc', 'operation_time'], sql
