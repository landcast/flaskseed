#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
import json
import jwt
import random
import requests

from src.models import db, session_scope, user_source, SmsLog,ThirdDateLog,SysUser,SysUserRole
from src.services import send_email, redis_store
import hashlib
from src.services import classin_service,do_query,email_service


BEARER_TOKEN = 'Bearer '

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    """
    swagger-doc: 'do login for registered user'
    required: ['username', 'password', 'usertype']
    req:
      username:
        description: 'login user name'
        type: 'string'
      password:
        description: 'login user password'
        type: 'string'
      usertype:
        description: 'login user type (Student, Teacher, SysUser)'
        type: 'string'
    res:
      Authorization:
        description: 'Athorization jwt http header'
        type: 'string'
    """
    user_name = request.json['username']
    password = request.json['password']
    user_type = request.json['usertype']
    email_service.sendEmail('lxf4456@163.com','ssssssssss','interview','interview1',1,'en')

    with session_scope(db) as session:
        user = session.query(user_source[user_type]).filter_by(
            username=user_name).first()
    if user:
        # check password
        if check_password_hash(getattr(user, 'password', ''), password):
            token = generate_jwt_token(current_app.config['JWT_HEADER'],
                                       user_name)
            return jsonify({**token, **{'id': getattr(user, 'id')}})
        else:
            return jsonify({'message': 'password check failed!'}), 401
    else:
        return jsonify({'message': user_name + ' not found!'}), 401


@auth.route('/logout')
def logout():
    return jsonify('')


@auth.route('/register', methods=['POST'])
def register():
    """
    swagger-doc: 'do register for new user'
    required: ['username', 'password', 'usertype', 'verify_code']
    req:
      username:
        description: 'login user name'
        type: 'string'
      password:
        description: 'login user password'
        type: 'string'
      usertype:
        description: 'login user type (Student, Teacher, SysUser)'
        type: 'string'
      verify_code:
        description: 'code sent by calling email verify or sms verify'
        type: 'string'
      first_name:
        description: 'first_name'
        type: 'string'
      last_name:
        description: 'last_name'
        type: 'string'
      code:
        description: '国家代码'
        type: 'int'
    res:
      Authorization:
        description: 'Athorization jwt http header'
        type: 'string'
    """
    current_app.logger.debug(request.json)
    user_name = request.json['username']
    user_type = request.json['usertype']
    verify_code = request.json['verify_code']
    check_target = redis_store.get('VC:' + user_name)

    code = request.json['code']


    firstName = ''
    lastName = ''

    if 'first_name' in request.json:
        firstName = request.json['first_name']
    if 'last_name' in request.json:
        lastName = request.json['last_name']

    if check_target:
        check_target = check_target.decode('utf8')
    else:
        check_target = 'None'
    current_app.logger.debug(verify_code + ' ' + check_target + ' ' +
                             str(verify_code != check_target))
    if verify_code != check_target:
        return jsonify({'message': 'verify code check failed'}), 500
    target_table = user_source[user_type]
    with session_scope(db) as session:
        # check existing username in all 3 tables
        found = False
        message = ''
        if target_table in user_source.values():
            result = session.execute(select([target_table]).where(
                target_table.username == user_name))
            current_app.logger.debug("table_checked.__name__ " +
                                     str(target_table.__name__))
            row1 = result.first()
            message = target_table.__name__ if (
                    row1 is not None) else ''
            found = found or (row1 is not None)
        else:
            return jsonify({
                "error": " not found {0} ".format(
                    target_table)
            }), 500

        if found:
            result.close()
            return jsonify({
                "error": "found {0} existing in {1}".format(
                    user_name,
                    message)
            }), 500
        # check if username is mobile or email, the mobile or email
        # should be unique in all 3 tables
        if '@' in user_name:
            for table_checked in user_source.values():
                result = session.execute(select([table_checked]).where(
                    table_checked.email == user_name))
                row1 = result.first()
                message = table_checked.__name__ + ' email' if (
                        row1 is not None) else ''
                found = found or (row1 is not None)
        else:
            for table_checked in user_source.values():
                result = session.execute(select([table_checked]).where(
                    table_checked.mobile == user_name))
                row1 = result.first()
                message = table_checked.__name__ + ' mobile' if (
                        row1 is not None) else ''
                found = found or (row1 is not None)
        if found:
            result.close()
            return jsonify({
                "error": "found {0} existing in {1}".format(
                    user_name,
                    message)
            }), 500
        email = user_name if '@' in user_name else None
        mobile = user_name if '@' not in user_name else None
        user = target_table(username=user_name,
                            password=generate_password_hash(
                                request.json['password']), state=1,
                            updated_by=user_name, email=email, mobile=mobile,nickname=user_name,first_name=firstName,last_name=lastName,nation = code)
        current_app.logger.debug('encrypted password:' + user.password)
        result = session.add(user)
        current_app.logger.debug(result)
    token = generate_jwt_token(current_app.config['JWT_HEADER'], user.username)
    user_id = getattr(user, 'id')
    token.update({'id': user_id})
    # handle acl redis record
    redis_key = 'ACL:' + user_name + ':' + user_type.lower() + ':' + str(
        user_id)
    value = hashlib.md5(str(user).encode('utf-8')).hexdigest()
    redis_store.set(redis_key, value)

    if user.mobile is not None:

        if code != '86':
            mobile = '00'+code+'-'+mobile
        current_app.logger.debug('code--->' + code+":"+mobile+"----->"+str(user_id))
        teacher_id = classin_service.register(mobile,mobile, request.json['password'], 0, 'en')
        current_app.logger.debug('target_table:' + user_type+'---table_id:'+str(user_id)+'-----teacher_id:'+str(teacher_id))
        thirdDateLog = ThirdDateLog(table_name = user_type,
                                   table_id = user_id,
                                   third_id = str(teacher_id),
                                    third_date = '',
                                   delete_flag = 'IN_FORCE')
        session.add(thirdDateLog)
        session.flush()


    return jsonify(token)


@auth.route('/smsverify', methods=['POST'])
def smsverify():
    """
    swagger-doc: 'send verify code by sms'
    required: ['mobile_no']
    req:
      mobile_no:
        description: 'mobile NO to receive verify code'
        type: 'string'
      country_code:
        description: 'country code, if omit, default to 86'
        type: 'string'
    res:
      verify_code:
        description: 'verify code sent to user mobile NO'
        type: 'string'
    """
    mobile_no = request.json['mobile_no']
    country_code = '86'
    verify_code = random.randint(100000, 999999)
    if 'country_code' in request.json:
        country_code = request.json['country_code']
    r = requests.post(
        current_app.config['EP_LOCATION'] + current_app.config['EP_SMS_PATH'],
        data=json.dumps({
            'type': 1,
            'userName': mobile_no,
            'registerType': 1,
            'countryCode': country_code,
            'code': str(verify_code)
        }), headers={'Content-type': 'application/json'})
    current_app.logger.debug(r.text)
    if r.json()['code'] == 0:
        with session_scope(db) as session:
            smslog = SmsLog(country_code=country_code, mobile=mobile_no,
                            content=verify_code, sms_channel='TX', state=1,
                            result_code=0, fee=5)
            session.add(smslog)
        redis_store.set('VC:' + mobile_no, str(verify_code))
        return jsonify({'verify_code': str(verify_code)})
    else:
        return jsonify({'message': r.json()['message']}), 500


@auth.route('/emailverify', methods=['POST'])
def email_verify():
    """
    swagger-doc: 'send verify code by email'
    required: ['email_address']
    req:
      email_address:
        description: 'email address to receive verify code'
        type: 'string'
    res:
      verify_code:
        description: 'verify code sent to user email address'
        type: 'string'
    """
    email_address = request.json['email_address']
    user_name = email_address
    user_type = 'SysUser'
    if 'username' in request.json:
        user_name = request.json['username']
    if 'usertype' in request.json:
        user_type = request.json['usertype']
    verify_code = random.randint(100000, 999999)
    send_email([email_address], subject='verify: ' + str(verify_code),
               body=user_name + ' - ' + user_type + ' - ' + str(verify_code))
    redis_store.set('VC:' + user_name, str(verify_code))
    return jsonify({'verify_code': str(verify_code)})


@auth.route('/resetpassword', methods=['POST'])
def resetpassword():
    """
    swagger-doc: 'do resetpassword with verify code sent by email or sms'
    required: ['username', 'password', 'verify_code']
    req:
      username:
        description: 'login user name'
        type: 'string'
      password:
        description: 'login user password'
        type: 'string'
      verify_code:
        description: 'code sent by calling email verify or sms verify'
        type: 'string'
    res:
      message:
        description: 'success message for reset password'
        type: 'string'
    """
    current_app.logger.debug(request.json)
    user_name = request.json['username']
    verify_code = request.json['verify_code']
    password = request.json['password']
    oldpassword = ''
    mobile = ''
    check_target = redis_store.get('VC:' + user_name)
    if check_target:
        check_target = check_target.decode('utf8')
    else:
        check_target = 'None'
    current_app.logger.debug(verify_code + ' ' + check_target + ' ' +
                             str(verify_code != check_target))
    if verify_code != check_target:
        return jsonify({'message': 'verify code check failed'}), 401
    with session_scope(db) as session:
        # check existing username in all 3 tables
        for table_checked in user_source.values():
            row1 = session.query(table_checked).filter(
                table_checked.username == user_name).one_or_none()
            current_app.logger.debug("table_checked.__name__ " +
                                     str(table_checked.__name__))
            if row1:
                # update password
                current_app.logger.debug('password: ' + row1.password)
#                oldpassword = row1.password
 #               mobile = row1.moble
                row1.password = generate_password_hash(password)
                current_app.logger.debug(
                    'new password: ' + row1.password)
                session.merge(row1)

 #               classin_service.editPasswort(mobile,row1.password,oldpassword,0,'en')

                return jsonify({'message': 'reset password succ!'})

    return jsonify({'message': user_name + ' not found!'}), 401


@auth.route('/sysUser', methods=['POST'])
def sysUser():
    """
    swagger-doc: 'do register for new user'
    required: ['username', 'password', 'usertype', 'verify_code']
    req:
      mobile:
        description: '手机号'
        type: 'string'
      name:
        description: '用户名'
        type: 'string'
      password:
        description: 'login user password'
        type: 'string'
      code:
        description: '国家代码'
        type: 'int'
      email:
        description: '邮箱'
        type: 'string'
      rolse:
        description: '角色id字符串 例如：1，2，3，4'
        type: 'string'
    res:
      id:
        description: '用户id'
        type: 'string'
    """
    current_app.logger.debug(request.json)
    mobile = request.json['mobile']
    name = request.json['name']
    email = request.json['email']
    rolse = request.json['rolse']
    user_type = 'SysUser'

    code = '86'
    if code in request.json:
        code = request.json['code']

    target_table = user_source[user_type]
    with session_scope(db) as session:
        sysUser = session.query(SysUser).filter_by(username=mobile).one_or_none()

        if sysUser is not None :
            return jsonify({
                "error": "found SysUser: {0}".format(
                    mobile)
            }), 500

        sysUser = SysUser(username=mobile,
                            password=generate_password_hash(
                                request.json['password']), state=1,
                            updated_by=getattr(g, current_app.config['CUR_USER'])['username'], email=email, mobile=mobile,nickname=mobile,nation = code,name=name)
        session.add(sysUser)
        session.flush()

        user_id = getattr(sysUser, 'id')
        for rolesId in rolse.split(','):
            sysUserRole = SysUserRole(sys_user_id=user_id,
                               role_definition_id=rolesId,
                           updated_by=getattr(g, current_app.config['CUR_USER'])['username'])
            session.add(sysUserRole)
            session.flush()


        if sysUser.mobile is not None:
            mobile = code+'-'+mobile
            if sysUser.nation is '86':
                mobile = sysUser.mobile

            teacher_id = classin_service.register(mobile,mobile, request.json['password'], 0, 'en')
            thirdDateLog = ThirdDateLog(table_name = 'sys_user',
                                        table_id = user_id,
                                        third_id = teacher_id,
                                        third_date = '',
                                        delete_flag = 'IN_FORCE')
            session.add(thirdDateLog)
            session.flush()


    return jsonify({'id':user_id })



@auth.route('/menu', methods=['POST'])
def menu():
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
              description: 'menu_id'
              type: 'integer'
            parent_id:
              description: '父类id'
              type: 'integer'
            parent_name:
              description: '菜单父类英文名字'
              type: 'integer'
            parent_name_zh:
              description: '菜单父类中文名称'
              type: 'integer'
            menu_name:
              description: '菜单英文名字'
              type: 'string'
            menu_name_zh:
              description: '菜单中文名字'
              type: 'integer'
            url:
              description: '地址'
              type: 'string'
            parent_url:
              description: '父类地址'
              type: 'integer'
    """
    j = request.json
    return jsonify(do_query(j, menu_sql))


def menu_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
            select m1.id,m2.id as parent_id,m2.`menu_name` as parent_name ,m2.`menu_name_zh` as parent_name_zh,m1.`menu_name`,m1.`menu_name_zh`,m1.url,m2.url as parent_url 
            from menu m1 left join  menu m2 on m2.id = m1.`parent_id` and m2.menu_type = 0
            where m1.menu_type = 1 and m1.id in (
                select rm.menu_id
                from sys_user_role sur,role_definition rd,role_menu rm
                where sur.`role_definition_id` = rd.id and rd.id = rm.role_definition_id 
                and sur.delete_flag = 'IN_FORCE' and rd.`delete_flag` = 'IN_FORCE' and rm.delete_flag = 'IN_FORCE'
            ''']

    sql.append("and sur.sys_user_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    sql.append(" )" )



    return ['id', 'parent_id','parent_name', 'parent_name_zh','menu_name','menu_name_zh','url','parent_url'], ''.join(sql)





def generate_jwt_token(header_name, username):
    payload = {
        current_app.config['JWT_SUBJECT_KEY']: username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'iss': 'src'
    }
    encoded = jwt.encode(payload, current_app.config['JWT_SECRET'],
                         algorithm=current_app.config['JWT_ALG'])
    return {header_name: BEARER_TOKEN + str(encoded, encoding='utf-8')}
