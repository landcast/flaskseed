#!/usr/bin/env python
from flask import jsonify, Blueprint, request,current_app
from src.services import do_query, datetime_param_sql_format


manger = Blueprint('manger', __name__)


@manger.route('/staff_query', methods=['POST'])
def query():
    """
    swagger-doc: 'do staff query'
    required: []
    req:
      page_limit:
        description: 'records in one page 分页中每页条数'
        type: 'integer'
      page_no:
        description: 'page no, start from 1 分页中页序号'
        type: 'integer'
      user_name:
        description: '用户名称'
        type: 'string'
      mobile:
        description: '电话'
        type: 'string'
      email:
        description: '邮件'
        type: 'string'
      role_id:
        description: '角色id'
        type: 'string'
      user_state:
        description: '用户状态'
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
              description: 'user id'
              type: 'integer'
            username:
              description: 'user name'
              type: 'string'
            mobile:
              description: 'mobile'
              type: 'string'
            mail:
              description: 'mail'
              type: 'string'
            created_at:
              description: 'order created at'
              type: 'string'
            role_name:
              description: '角色名称'
              type: 'string'
            state:
              description: 'state'
              type: 'integer'
            sys_user_id:
              description: 'sys_user_id'
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
    sql = ['''
    select su.id,su.username,su.mobile,su.email,su.`created_at`,rd.role_name,su.state,sur.sys_user_id
    from sys_user su,sys_user_role sur,role_definition rd 
    where su.`id`=sur.sys_user_id and sur.role_definition_id = rd.id
    ''']
    if 'user_name' in params.keys():
        sql.append(' and su.username like :user_name')
    if 'mobile' in params.keys():
        sql.append(' and su.mobile = :mobile')
    if 'email' in params.keys():
        sql.append(' and su.email = :email')
    if 'role_id' in params.keys():
        sql.append(' and rd.id = :role_id')
    if 'user_state' in params.keys():
        sql.append(' and su.state = :user_state')
    # current_app.logger.debug(sql)
    return ['id', 'username', 'mobile', 'email', 'created_at',
            'role_name', 'state'], ''.join(sql)


@manger.route('/student_course', methods=['POST'])
def student_course():
    """
    swagger-doc: 'do student course query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_id:
        description: '学生id'
        type: 'string'
      student_name:
        description: 'student name'
        type: 'string'
      course_name:
        description: 'course name'
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
            teacher_name:
              description: 'teachaer name'
              type: 'string'
            start:
              description: 'course start'
              type: 'string'
            end:
              description: 'course end'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['course_time']),
    return jsonify(do_query(j, student_course_sql))


def student_course_sql(params):
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
		t.`nickname` as teacher_name,
		cs.start,cs.end
    from `order` o, student s, teacher t, course c,`course_schedule`cs 
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.`id` = cs.course_id
    ''']
    sql.append("and s.id =" + params['student_id'])
    if 'course_name' in params.keys():
        sql.append(
            ' and （c.course_name like :course_name or c.course_name_zh '
            'like:course_name)')
    if 'student_name' in params.keys():
        sql.append(
            ' and s.username like :student_name ')
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

    return ['id', 'course_name', 'finish', 'classes_number', 'teacher_name',
            'start', 'end'], ''.join(sql)

