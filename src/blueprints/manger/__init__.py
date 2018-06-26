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
    and su.`delete_flag` = 'IN_FORCE' and sur.`delete_flag` = 'IN_FORCE' and rd.`delete_flag` = 'IN_FORCE' 
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
        and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' 
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


@manger.route('/student_allot', methods=['POST'])
def allot_query():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_name:
        description: 'student_name'
        type: 'string'
      mobile:
        description: 'mobile'
        type: 'string'
      email:
        description: 'email'
        type: 'string'
      state:
        description: 'state '
        type: 'string'
      student_from:
        description: 'studeng from'
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
              description: 'id'
              type: 'integer'
            username:
              description: '学生账号'
              type: 'integer'
            family_name:
              description: 'family_name'
              type: 'string'
            given_name:
              description: 'given_name'
              type: 'string'
            mobile:
              description: 'mobile'
              type: 'string'
            email:
              description: 'email'
              type: 'string'
            created_at:
              description: 'created at'
              type: 'string'
            channel_name:
              description: 'channel name'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
            su_family_name:
              description: '课程顾问family_name'
              type: 'string'
            su_given_name:
              description: '课程顾问given_name'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, student_allot_sql))


def student_allot_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select s.id,s.username,s.`family_name`,s.`given_name`,s.mobile,s.email,s.`created_at`,c.channel_name,s.state,su.family_name as su_family_name,su.given_name as su_given_name
    from student s left join sys_user su on  s.consultant_id = su.id   ,enrollment e,channel c
    where 
     s.id = e.`student_id` and e.`channel_id` = c.id
    and s.`delete_flag` = 'IN_FORCE' and e.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'student_name' in params.keys():
        sql.append(' and s.family_name like:student_name')

    if 'mobile' in params.keys():
        sql.append(' and s.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and s.email =:email')

    if 'state' in params.keys():
        sql.append(' and s.state =:state')

    if 'student_from' in params.keys():
        sql.append(' and c.channel_name like:student_from')

    return ['id', 'username', 'family_name', 'given_name', 'mobile',
            'email', 'created_at', 'channel_name', 'state', 'su_family_name', 'su_given_name'], ''.join(sql)


@manger.route('/thacher_check', methods=['POST'])
def thacher_check():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: 'teacher_name'
        type: 'string'
      mobile:
        description: 'mobile'
        type: 'string'
      email:
        description: 'email'
        type: 'string'
      state:
        description: 'state '
        type: 'string'
      update_at_start:
        description: 'update_at start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      update_at_end:
        description: 'update_at end in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: 'id'
              type: 'integer'
            username:
              description: '学生账号'
              type: 'integer'
            mobile:
              description: 'mobile'
              type: 'string'
            email:
              description: 'email'
              type: 'string'
            update_at:
              description: 'update at'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, thacher_check_sql))


def thacher_check_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select t.id,t.username,t.mobile,t.email,t.`updated_at`,t.state
    from teacher t   where
    t.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys():
        sql.append(' and s.state =:state')

    if 'update_at_start' in params.keys() \
            and 'update_at_end' in params.keys():
        sql.append(
            ' and t.update_at between :created_at_start and :created_at_end')

    return ['id', 'username', 'family_name', 'given_name', 'mobile',
            'email', 'created_at', 'channel_name', 'state', 'su_family_name', 'su_given_name'], ''.join(sql)


@manger.route('/thacher_interview', methods=['POST'])
def thacher_interview():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: 'teacher_name'
        type: 'string'
      interview_name:
        description: 'interview_name'
        type: 'string'
      mobile:
        description: 'mobile'
        type: 'string'
      email:
        description: 'email'
        type: 'string'
      state:
        description: 'state '
        type: 'string'
      interview_at:
        description: '面试时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: 'id'
              type: 'integer'
            course_id:
              description: '课程id'
              type: 'integer'
            username:
              description: '教师账号'
              type: 'integer'
            mobile:
              description: 'mobile'
              type: 'string'
            email:
              description: 'email'
              type: 'string'
            course_name:
              description: '课程名称'
              type: 'string'
            interview_name:
              description: '面试人'
              type: 'string'
            start:
              description: '面试开始时间'
              type: 'string'
            end:
              description: '面试结束时间'
              type: 'string'
            courseware_num:
              description: '课件个数0为上传，>0已经上传'
              type: 'integer'
    """
    j = request.json
    return jsonify(do_query(j, thacher_interview_sql))


def thacher_interview_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select t.id,c.id as course_id,t.username,t.mobile,t.email,c.`course_name`,i.`updated_by` as interview_name,i.`start`,i.`end`,t.state
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num
    from teacher t left join interview i  on i.teacher_id = t.id  and i.`delete_flag` = 'IN_FORCE' and i.`state` <> 99
    left join course c on c.`primary_teacher_id` = t.id  and c.`delete_flag` = 'IN_FORCE'  and c.`state` <> 99 and c.class_type = 3
    where t.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys():
        sql.append(' and s.state =:state')

    if 'interview_at' in params.keys():
        sql.append(
            ' and i.`start` >:interview_at and i.`end` <: interview_at')

    if 'interview_name' in params.keys():
        sql.append(' and i.updated_by like:interview_name')

    return ['id', 'course_id', 'username', 'mobile', 'email',
            'course_name', 'interview_name', 'start', 'end', 'state', 'courseware_num'], ''.join(sql)


@manger.route('/students', methods=['POST'])
def students_query():
    """
    swagger-doc: 'do students query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_name:
        description: 'student_name'
        type: 'string'
      mobile:
        description: 'mobile'
        type: 'string'
      email:
        description: 'email'
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
              description: 'id'
              type: 'integer'
            username:
              description: '学生账号'
              type: 'integer'
            family_name:
              description: 'family_name'
              type: 'string'
            given_name:
              description: 'given_name'
              type: 'string'
            mobile:
              description: 'mobile'
              type: 'string'
            email:
              description: 'email'
              type: 'string'
            create_at:
              description: 'create_at'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, students_sql))


def students_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select s.id,s.username,s.`family_name`,s.`given_name`,s.mobile,s.email,s.`created_at`
    from student s
    where s.`delete_flag` = 'IN_FORCE'  
    ''']

    if 'student_name' in params.keys():
        sql.append(' and s.username like:student_name')

    if 'mobile' in params.keys():
        sql.append(' and s.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and s.email =:email')

    if 'state' in params.keys():
        sql.append(' and s.state =:state')

    return ['id', 'username', 'family_name', 'given_name', 'mobile',
            'email', 'created_at'], ''.join(sql)


@manger.route('/thacher_tryout', methods=['POST'])
def thacher_tryout():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: 'teacher_name'
        type: 'string'
      class_at:
        description: 'class_at 上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      courseware_state:
        description: '课件状态0：没有，1：有'
        type: 'string'
      course_schedule_state:
        description: '课程状态，1：未上，2：已经上课，2：取消，4：问题课'
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
              description: 'id'
              type: 'integer'
            teacher_name:
              description: '教师账号'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            student_name:
              description: '学生账号'
              type: 'string'
            grade:
              description: '年级'
              type: 'string'
            start:
              description: '开始时间'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            courseware_num:
              description: '课件个数，0：未上传 >0已经上传'
              type: 'string'
            course_schedule_state:
              description: '课程状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, thacher_tryout_sql))


def thacher_tryout_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select * from (select c.id,t.username as teacher_name,c.`course_name`,s.username as student_name,s.`grade`,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`state` as course_schedule_state
    from course c,teacher t ,student s,`order` o,course_schedule cs
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = t.id and c.id = cs.course_id
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` = 3 )  t
    ''']

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` >:class_at and t.`end` <:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =：courseware_state')

    return ['id', 'teacher_name', 'course_name', 'student_name', 'grade',
            'start', 'end','course_schedule_state'], ''.join(sql)


@manger.route('/student_tryout', methods=['POST'])
def student_tryout_query():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: 'teacher_name'
        type: 'string'
      class_at:
        description: 'class_at 上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      courseware_state:
        description: '课件状态0：没有，1：有'
        type: 'string'
      course_schedule_state:
        description: '课程状态，1：未上，2：已经上课，2：取消，4：问题课'
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
              description: 'id'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'integer'
            open_grade:
              description: '开设年级'
              type: 'string'
            teacher_name:
              description: '教师账号'
              type: 'string'
            student_name:
              description: '学生账号'
              type: 'string'
            start:
              description: '开始时间'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            courseware_num:
              description: '课件数量'
              type: 'string'
            course_schedule_state:
              description: '课程状态，1：未上，2：已经上课，2：取消，4：问题课'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, student_tryout_sql))


def student_tryout_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select * from (select c.id,c.`course_name`,c.open_grade,t.username as teacher_name,s.username as student_name,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`state` as course_schedule_state
    from course c,teacher t ,student s,`order` o,course_schedule cs
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = t.id and c.id = cs.course_id
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` = 3 )  t
    ''']

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` >:class_at and t.`end` <:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =：courseware_state')

    return ['id', 'teacher_name', 'course_name', 'student_name', 'level',
            'start', 'end'], ''.join(sql)


@manger.route('/course_ware', methods=['POST'])
def course_ware_query():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      classroom_name:
        description: '课节名称'
        type: 'string'
      course_ware_name:
        description: '课件名称'
        type: 'string'
      subject_name:
        description: '课包名称'
        type: 'string'
      teacher_name:
        description: '教师名称'
        type: 'string'
      state:
        description: '待审核：BEFORE_CHECK，审核通过：CHECK_PASSED，审核驳回：CHECK_DENY'
        type: 'string'
      class_at:
        description: 'class_at 上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: 'id'
              type: 'integer'
            ware_name:
              description: '课件名称'
              type: 'integer'
            room_title:
              description: '课节，房间名称'
              type: 'string'
            subject_name:
              description: '课包名称'
              type: 'string'
            teacher_name:
              description: '教师账号'
              type: 'string'
            created_at:
              description: '课件创建时间'
              type: 'string'
            state:
              description: '课件状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, course_ware_sql))


def course_ware_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select csw.id,csw.ware_name,cc.room_title,su.subject_name,t.`username` as teacher_name,csw.`created_at`,csw.`checked_result` as state
    from course c,teacher t ,course_schedule cs,course_classroom cc,courseware csw,subject su
    where c.`primary_teacher_id` = t.id and c.id = cs.`course_id` and cs.id = cc.course_schedule_id and cc.room_id = csw.room_id and c.subject_id = su.id
    and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and cc.`delete_flag` = 'IN_FORCE' and csw.`delete_flag` = 'IN_FORCE' and su.`delete_flag` = 'IN_FORCE' 
   
    ''']

    if 'classroom_name' in params.keys():
        sql.append(' and cc.room_title like:classroom_name')

    if 'course_ware_name' in params.keys():
        sql.append(' and csw.ware_name like:course_ware_name')

    if 'subject_name' in params.keys():
        sql.append(' and su.subject_name like:subject_name')

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'state' in params.keys():
        sql.append(' and csw.`checked_result` =:state')

    if 'class_at' in params.keys() :
        sql.append(
            ' and cs.`start` >:class_at and cs.`end` <:class_at')

    return ['id', 'ware_name', 'room_title', 'subject_name', 'teacher_name',
            'created_at', 'state'], ''.join(sql)


@manger.route('/thacher_common', methods=['POST'])
def thacher_common():
    """
    swagger-doc: 'do allot query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: 'teacher_name'
        type: 'string'
      class_at:
        description: 'class_at 上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      courseware_state:
        description: '课件状态0：没有，1：有'
        type: 'string'
      course_schedule_state:
        description: '课程状态，1：未上，2：已经上课，2：取消，4：问题课'
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
              description: 'id'
              type: 'integer'
            teacher_name:
              description: '教师账号'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            student_name:
              description: '学生账号'
              type: 'string'
            grade:
              description: '年级'
              type: 'string'
            start:
              description: '开始时间,如果没有就是带排课'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            courseware_num:
              description: '课件个数，0：未上传 >0已经上传'
              type: 'string'
            course_schedule_state:
              description: '课程状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, thacher_common_sql))


def thacher_common_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select * from (select c.id,t.username as teacher_name,c.`course_name`,s.username as student_name,s.`grade`,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`state` as course_schedule_state
    from course c left join course_schedule cs on c.id = cs.course_id and cs.`delete_flag` = 'IN_FORCE'  ,teacher t ,student s,`order` o
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = t.id 
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` < 3 )  t
    ''']

    if 'teacher_name' in params.keys():
        sql.append(' and t.username like:teacher_name')

    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` >:class_at and t.`end` <:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =：courseware_state')

    return ['id', 'teacher_name', 'course_name', 'student_name', 'grade',
            'start', 'end','course_schedule_state'], ''.join(sql)


@manger.route('/orders', methods=['POST'])
def orders_query():
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
      order_id:
        description: '订单编号'
        type: 'string'
      subject_name:
        description: '课包名称'
        type: 'string'
      updated_by:
        description: 'updated by 下单人'
        type: 'string'
      created_at_start:
        description: '订单创建时间开始，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      created_at_end:
        description: '订单创建时间结束，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      order_type:
        description: 'order type 订单类型'
        type: 'string'
      order_state:
        description: 'order state 订单状态'
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
            subject_name:
              description: '课包 name'
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
    return jsonify(do_query(
        datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
        orders_query_sql))


def orders_query_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    sql = ['''
    select o.id, su.subject_name, c.classes_number, o.order_type, o.state,
        o.updated_by, o.created_at, t.nickname, s.nickname, o.amount
    from `order` o, student s, teacher t, course c, subject su
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id 
    ''']
    if 'order_id' in params.keys():
        sql.append(' and o.id = :course_id')
    if 'subject_name' in params.keys():
        sql.append(' and (su.subject_name = :subject_name or su.subject_name_zh = :subject_name)')
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

    # current_app.logger.debug(sql)
    return ['id', 'subject_name', 'classes_number', 'order_type', 'order_state',
            'updated_by', 'created_at', 'teacher_name', 'student_name',
            'order_amount'], ''.join(sql)


