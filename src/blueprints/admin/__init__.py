#!/usr/bin/env python
from flask import jsonify, Blueprint, request
from src.services import do_query, datetime_param_sql_format


admin = Blueprint('admin', __name__)


@admin.route('/staff_query', methods=['POST'])
def query():
    """
    swagger-doc: 'do order query'
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
    """
    j = request.json
    return jsonify(do_query(
        generate_sql))


def generate_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    sql = ['''
    select su.id,su.username,su.mobile,su.email,su.`created_at`,rd.role_name,su.state
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
