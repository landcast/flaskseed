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
from src.services import classin_service

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

    code = '86'
    if code in request.json:
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
        for table_checked in user_source.values():
            result = session.execute(select([table_checked]).where(
                table_checked.username == user_name))
            current_app.logger.debug("table_checked.__name__ " +
                                     str(table_checked.__name__))
            row1 = result.first()
            message = table_checked.__name__ if (
                    row1 is not None) else ''
            found = found or (row1 is not None)
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

        if code is not '86':
            mobile = code+'-'+mobile
        current_app.logger.debug('code--->' + code+":"+mobile)
        teacher_id = classin_service.register(mobile,mobile, request.json['password'], 0, 'en')
        current_app.logger.debug('target_table:' + target_table+'---table_id:'+str(user_id)+'-----teacher_id:'+teacher_id)
        thirdDateLog = ThirdDateLog(table_name = target_table,
                                   table_id = user_id,
                                   third_id = teacher_id,
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
                oldpassword = row1.password
                mobile = row1.moble
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
        current_app.logger.debug('user--->'+str(user_id))
        for rolesId in rolse.split(','):
            current_app.logger.debug('rolesId--->'+str(rolesId))
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
