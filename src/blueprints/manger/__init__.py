#!/usr/bin/env python
from flask import jsonify, Blueprint, request,current_app
from src.services import do_query, datetime_param_sql_format
from src.models import db, session_scope,Teacher,Interview,CourseSchedule, \
    CourseSchedule,StudySchedule,Homework,CourseSchedule,CourseClassroom
from src.services import do_query, datetime_param_sql_format
from src.services import live_service
from src.models import ClassroomRoleEnum, ClassroomDeviceEnum
from flask import g


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
              description: '用户id'
              type: 'integer'
            username:
              description: '用户账号'
              type: 'string'
            mobile:
              description: '手机'
              type: 'string'
            mail:
              description: '邮箱'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            role_name:
              description: '角色名称'
              type: 'string'
            state:
              description: '用户状态'
              type: 'integer'
            sys_user_id:
              description: '用户角色关联id'
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
        select su.id,su.name as username,su.mobile,su.email,su.`created_at`,
        (select GROUP_CONCAT(role_name) from sys_user_role sur1,role_definition rd1 where sur1.role_definition_id = rd1.id and  sur1.sys_user_id = su.id  and sur1.`delete_flag` = 'IN_FORCE' and rd1.`delete_flag` = 'IN_FORCE') as role_name,
        su.state,sur.id
        from sys_user su left join sys_user_role sur on su.id = sur.sys_user_id and sur.`delete_flag` = 'IN_FORCE'
        where su.`delete_flag` = 'IN_FORCE' 
    ''']
    if 'user_name' in params.keys():
        sql.append(" and su.name like '%")
        sql.append(params['username'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(" and su.mobile like '%")
        sql.append(params['mobile'])
        sql.append("%'")

    if 'email' in params.keys():
        sql.append(" and su.email like '%")
        sql.append(params['email'])
        sql.append("%'")
    if 'role_id' in params.keys():
        sql.append(' and sur.role_definition_id = :role_id')
    if 'user_state' in params.keys():
        sql.append(' and su.state = :user_state')

    sql.append(' order by su.id desc')

    current_app.logger.debug(sql)
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
        description: '学生名称'
        type: 'string'
      course_name:
        description: '课程名称'
        type: 'string'
      course_time:
        description: '课程时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_status:
        description: '课程状态 1：上完,2:未上'
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
              description: '课程id'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            finish:
              description: '已经上过的课程数量'
              type: 'integer'
            classes_number:
              description: '全部课程数量'
              type: 'integer'
            teacher_name:
              description: '教师名称'
              type: 'string'
            start:
              description: '课程开始时间'
              type: 'string'
            end:
              description: '课程结束时间'
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
		concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,
		cs.start,cs.end
    from `order` o, student s, teacher t, course c,`course_schedule`cs 
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.`id` = cs.course_id
        and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' 
    ''']
    sql.append("and s.id =" + params['student_id'])
    if 'course_name' in params.keys():
        sql.append(" and (c.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or c.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'student_name' in params.keys():
        sql.append(" and s.name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name)  like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'course_time' in params.keys():
        sql.append(
            ' and cs.start <:course_time and cs.end >:course_time')
    if 'course_status' in params.keys() \
            and params['course_status'] == '1':
        sql.append(' and cs.end >=now()')
    if 'course_status' in params.keys() \
            and params['course_status'] == '2':
        sql.append(' and cs.end < now()')

    sql.append(' order by o.id desc')

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
        description: '学生名称'
        type: 'string'
      mobile:
        description: '手机号'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      state:
        description: '学生状态 '
        type: 'string'
      student_from:
        description: '学生来源'
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
              description: '学生id'
              type: 'integer'
            username:
              description: '学生账号'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            mobile:
              description: '手机号'
              type: 'string'
            email:
              description: '邮箱'
              type: 'string'
            created_at:
              description: '注册时间'
              type: 'string'
            channel_name:
              description: '渠道名称'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
            su_name:
              description: '课程顾问名称'
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
    select s.id,s.username,s.name as student_name,s.mobile,s.email,s.`created_at`,c.channel_name,s.state,su.name as su_name
    from student s left join sys_user su on  s.consultant_id = su.id   ,enrollment e,channel c
    where 
     s.id = e.`student_id` and e.`channel_id` = c.id
    and s.`delete_flag` = 'IN_FORCE' and e.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'student_name' in params.keys():
        sql.append(" and s.name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(' and s.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and s.email =:email')

    if 'state' in params.keys():
        sql.append(' and s.state =:state')

    if 'student_from' in params.keys():
        sql.append(" and c.channel_name like '%")
        sql.append(params['student_from'])
        sql.append("%'")
    sql.append(' order by s.id desc')

    return ['id', 'username','student_name', 'mobile',
            'email', 'created_at', 'channel_name', 'state','su_name'], ''.join(sql)


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
        description: '教师名称'
        type: 'string'
      mobile:
        description: '手机号'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      state:
        description: '教师状态 '
        type: 'string'
      update_at_start:
        description: '教师注册开始时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      update_at_end:
        description: ' 教师注册结束时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: '教师id'
              type: 'integer'
            teacher_name:
              description: '教师名称'
              type: 'integer'
            mobile:
              description: '手机号'
              type: 'string'
            email:
              description: '邮箱'
              type: 'string'
            update_at_start:
              description: '更新时间'
              type: 'string'
            update_at_end:
              description: '更新时间'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['update_at']),
    return jsonify(do_query(j, thacher_check_sql))


def thacher_check_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select t.id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,t.mobile,t.email,t.`updated_at`,t.state
    from teacher t   where
    t.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name)  like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys():
        sql.append(' and t.state =:state')

    if 'update_at_start' in params.keys() \
            and 'update_at_end' in params.keys():
        sql.append(
            ' and t.updated_at between :update_at_start and :update_at_end')

    sql.append(' order by t.id desc')

    return ['id', 'teacher_name', 'mobile', 'email', 'updated_at',
            'state'], ''.join(sql)


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
        description: '教师名称'
        type: 'string'
      interview_name:
        description: '面试人名称'
        type: 'string'
      mobile:
        description: '手机号'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      state:
        description: '状态 '
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
              description: '教师id'
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
            state:
              description: '教师状态'
              type: 'string'
            integerview_state:
              description: '面试状态'
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
    select t.id,c.id as course_id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as username,t.mobile,t.email,c.`course_name`,i.`updated_by` as interview_name,i.`start`,i.`end`,t.state,i.state as integerview_state,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num
    from teacher t
    left join course c on c.`primary_teacher_id` = t.id  and c.`delete_flag` = 'IN_FORCE'  and c.`state` <> 99 and c.class_type = 3
    ,interview i left join sys_user su on i.interviewer_id = su.id 
    where  t.`delete_flag` = 'IN_FORCE' and t.state = 'WAIT_FOR_INTERVIEW' and i.teacher_id = t.id  and i.`delete_flag` = 'IN_FORCE' and i.`state` <> 99 and i.state in(2,3,4,5)
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name) like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys():
        sql.append(' and t.state =:state')

    if 'interview_at' in params.keys():
        sql.append(
            ' and i.`start` <:interview_at and i.`end` >:interview_at')

    if 'interview_name' in params.keys():
        sql.append(" and su.name like '%")
        sql.append(params['interview_name'])
        sql.append("%'")
    sql.append(' order by t.id desc')

    return ['id', 'course_id', 'username', 'mobile', 'email',
            'course_name', 'interview_name', 'start', 'end', 'state','integerview_state','courseware_num'], ''.join(sql)


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
        description: '学生名称'
        type: 'string'
      student_id:
        description: '学生id'
        type: 'string'
      gender:
        description: '年级'
        type: 'string'
      parent_mobile:
        description: '家长手机号'
        type: 'string'
      category_1:
        description: '一级分类id'
        type: 'string'
      category_2:
        description: '二级id'
        type: 'string'
      channel_id:
        description: '渠道id'
        type: 'string'
      created_at_start:
        description: '订单创建时间开始，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      created_at_end:
        description: '订单创建时间结束，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
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
              description: '学生id'
              type: 'integer'
            username:
              description: '学生账号'
              type: 'string'
            student_name:
              description: '学生名称'
              type: 'string'
            mobile:
              description: '手机号'
              type: 'string'
            email:
              description: '邮箱'
              type: 'string'
            create_at:
              description: '注册时间'
              type: 'string'
            state:
              description: '状态'
              type: 'string'
            gender:
              description: '年级'
              type: 'string'
            parent_mobile:
              description: '家长联系电话'
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
    select s.id,s.`created_at`,s.name as username,s.parent_mobile,s.gender,c.channel_name,s.gender
    from student s 
    left join  student_subject ss on s.id = ss.student_id and ss.`delete_flag` = 'IN_FORCE'  
    left join subject su on ss.`subject_id` = su.id and su.state <> 99 and su.`delete_flag` = 'IN_FORCE'
    left join subject_category sc on su.`subject_category_id` = sc.id and sc.state <> 99 and sc.`delete_flag` = 'IN_FORCE'
    left join  channel c on s.channel_id = c.id and c.`delete_flag` = 'IN_FORCE' 
    where s.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'student_name' in params.keys():
        sql.append(" and s.name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'student_id' in params.keys():
        sql.append(' and s.id =:student_id')

    if 'gender' in params.keys():
        sql.append(' and s.gender =:gender')

    if 'parent_mobile' in params.keys():
        sql.append(' and s.parent_mobile =:parent_mobile')
    if 'category_1' in params.keys():
        sql.append(' and sc.`curriculum_id` =:category_1')
    if 'category_2' in params.keys():
        sql.append(' and sc.id =:category_2')
    if 'channel_id' in params.keys():
        sql.append(' and c.id =:channel_id')
    if 'created_at_start' in params.keys() \
        and 'created_at_end' in params.keys():
        sql.append(' and s.created_at between :created_at_start and :created_at_end')
    sql.append(' order by s.id desc')

    return ['id', 'created_at','username', 'parent_mobile',
            'gender', 'channel_name','gender'], ''.join(sql)


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
        description: '教师名称'
        type: 'string'
      class_at:
        description: '上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: '课程id'
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
    datetime_param_sql_format(j, ['class_at']),
    return jsonify(do_query(j, thacher_tryout_sql))


def thacher_tryout_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select * from (select c.id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,c.`course_name`,s.name as student_name,s.`grade`,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`state` as course_schedule_state
    from course c,teacher t ,student s,`order` o,course_schedule cs
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = t.id and c.id = cs.course_id
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` = 3 )  t where 1=1
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and t.teacher_name like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")

    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` >:class_at and t.`end` <:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =:courseware_state')
    sql.append(' order by t.id desc')


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
        description: '教师名称'
        type: 'string'
      class_at:
        description: '上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: '课程id'
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
              description: '课程状态，枚举name'
              type: 'string'
            study_schedule_id:
              description: 'study_schedule_id'
              type: 'string'
            course_schedule_id:
              description: 'course_schedule_id'
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
    select * from (select c.id,c.`course_name`,c.open_grade,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,s.name as student_name,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`schedule_type` as course_schedule_state,ss.id as study_schedule_id,cs.id as course_schedule_id
    from course c,teacher t ,student s,`order` o,course_schedule cs,study_schedule ss
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = s.id and c.id = cs.course_id and cs.id = ss.course_schedule_id
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` = 3 )  t where 1=1
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and t.teacher_name like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` <:class_at and t.`end` >:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =:courseware_state')
    if 'course_schedule_state' in params.keys():
        sql.append(
            ' and t.course_schedule_state =:course_schedule_state')
    sql.append(' order by t.id desc')
    return ['id', 'course_name', 'open_grade', 'teacher_name', 'student_name',
            'start', 'end','courseware_num','course_schedule_state','study_schedule_id','course_schedule_id'], ''.join(sql)


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
      course_name:
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
            course_name:
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
    select csw.id,csw.ware_name,cc.room_title,c.course_name,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,csw.`created_at`,csw.`checked_result` as state
    from course c,teacher t ,course_schedule cs,course_classroom cc,courseware csw,subject su
    where c.`primary_teacher_id` = t.id and c.id = cs.`course_id` and cs.id = cc.course_schedule_id and cc.room_id = csw.room_id and c.subject_id = su.id
    and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and cc.`delete_flag` = 'IN_FORCE' and csw.`delete_flag` = 'IN_FORCE' and su.`delete_flag` = 'IN_FORCE' 
   
    ''']

    if 'classroom_name' in params.keys():
        sql.append(" and cc.room_title like '%")
        sql.append(params['classroom_name'])
        sql.append("%'")

    if 'course_ware_name' in params.keys():
        sql.append(" and csw.ware_name like '%")
        sql.append(params['course_ware_name'])
        sql.append("%'")

    if 'course_name' in params.keys():
        sql.append(" and c.course_name  like '%")
        sql.append(params['course_name'])
        sql.append("%'")
    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name)  like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'state' in params.keys():
        sql.append(' and csw.`checked_result` =:state')

    if 'class_at' in params.keys() :
        sql.append(
            ' and cs.`start` <:class_at and cs.`end` >:class_at')
    sql.append(' order by c.id desc')
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
        description: '教师名称'
        type: 'string'
      class_at:
        description: '上课时间 start in sql format YYYY-mm-dd HH:MM:ss.SSS'
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
            course_schedule_id:
              description: '课表id,如果为null就是为排课，存在id已经排课'
              type: 'string'
    """
    j = request.json
    datetime_param_sql_format(j, ['class_at']),
    return jsonify(do_query(j, thacher_common_sql))


def thacher_common_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select * from (select c.id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,c.`course_name`,s.name as student_name,s.`grade`,cs.`start`,cs.`end`,
    (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = c.id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num,
    cs.`state` as course_schedule_state,cs.id as course_schedule_id
    from course c left join course_schedule cs on c.id = cs.course_id and cs.`delete_flag` = 'IN_FORCE'  ,teacher t ,student s,`order` o
    where c.`primary_teacher_id` = t.id and o.course_id = c.id and o.student_id = t.id 
    and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and o.`delete_flag` = 'IN_FORCE' 
    and c.`class_type` < 3 )  t where 1=1
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and t.teacher_name like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'class_at' in params.keys() :
        sql.append(
            ' and t.`start` <:class_at and t.`end` >:class_at')
    if 'courseware_state' in params.keys():
        sql.append(
            ' and t.courseware_num =:courseware_state')
    sql.append(' order by t.id desc')
    return ['id', 'teacher_name', 'course_name', 'student_name', 'grade',
            'start', 'end','course_schedule_state','course_schedule_id'], ''.join(sql)


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
      payment_state:
        description: '支付状态'
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
              description: '上课总节数'
              type: 'integer'
            order_type:
              description: '订单类型'
              type: 'integer'
            order_state:
              description: '订单状态'
              type: 'integer'
            updated_by:
              description: '订单更新时间'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            student_name:
              description: '学生名称'
              type: 'string'
            order_amount:
              description: '订单金额'
              type: 'integer'
            payment_state:
              description: '支付状态'
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
        o.updated_by, o.created_at, concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name, s.name  as student_name, o.amount as order_amount ,o.payment_state
    from `order` o, student s, teacher t, course c, subject su
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id 
    ''']
    if 'order_id' in params.keys():
        sql.append(' and o.id = :order_id')
    if 'subject_name' in params.keys():
        sql.append(" and (su.subject_name  like '%")
        sql.append(params['subject_name'])
        sql.append("%'")
        sql.append(" or su.subject_name_zh like '%")
        sql.append(params['subject_name'])
        sql.append("%')")
    if 'order_type' in params.keys():
        sql.append(' and o.order_type = :order_type')
    if 'payment_state' in params.keys():
        sql.append(' and o.payment_state = :payment_state')
    if 'order_state' in params.keys():
        sql.append(' and o.state = :order_state')
    if 'updated_by' in params.keys():
        sql.append(' and o.updated_by = :updated_by')
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and :created_at_end')
    sql.append(' order by o.id desc')
    current_app.logger.debug(sql)
    return ['id', 'subject_name', 'classes_number', 'order_type', 'order_state',
            'updated_by', 'created_at', 'teacher_name', 'student_name',
            'order_amount','payment_state'], ''.join(sql)


@manger.route('/refunds', methods=['POST'])
def refund_query():
    """
    swagger-doc: 'do refund query'
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
      payment_state:
        description: '支付状态'
        type: 'string'
      created_at_start:
        description: '订单创建时间开始，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      created_at_end:
        description: '订单创建时间结束，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      updated_by:
        description: 'updated by 下单人'
        type: 'string'
      order_type:
        description: 'order type 订单类型'
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
            order_type:
              description: '订单类型'
              type: 'integer'
            order_state:
              description: '订单状态'
              type: 'integer'
            updated_by:
              description: '订单更新人'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            student_name:
              description: '学生名称'
              type: 'string'
            order_amount:
              description: '订单金额'
              type: 'integer'
            payment_state:
              description: '支付状态'
              type: 'integer'
    """
    j = request.json
    return jsonify(do_query(
        datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
        refund_query_sql))


def refund_query_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    sql = ['''
    select o.id, su.subject_name,  o.order_type, o.state,
        o.updated_by, o.created_at, concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name, s.name  as student_name, o.amount as order_amount,o.payment_state
    from `order` o, student s, teacher t, course c, subject su
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id and o.payment_state in (4,5,6,7)
    ''']
    if 'order_id' in params.keys():
        sql.append(' and o.id = :order_id')
    if 'subject_name' in params.keys():
        sql.append(" and (su.subject_name  like '%")
        sql.append(params['subject_name'])
        sql.append("%'")
        sql.append(" or su.subject_name_zh like '%")
        sql.append(params['subject_name'])
        sql.append("%')")
    if 'order_type' in params.keys():
        sql.append(' and o.order_type = :order_type')
    if 'payment_state' in params.keys():
        sql.append(' and o.payment_state = :payment_state')
    if 'order_state' in params.keys():
        sql.append(' and o.state = :order_state')
    if 'updated_by' in params.keys():
        sql.append(' and o.updated_by = :updated_by')
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and :created_at_end')
    sql.append(' order by o.id desc')
    current_app.logger.debug(sql)
    return ['id', 'subject_name', 'order_type', 'order_state',
            'updated_by', 'created_at', 'teacher_name', 'student_name',
            'order_amount','payment_state'], ''.join(sql)


@manger.route('/thacher_apponit', methods=['POST'])
def thacher_apponit():
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
        description: '教师名称'
        type: 'string'
      mobile:
        description: '手机号'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      state:
        description: '状态 '
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
              description: '教师id'
              type: 'integer'
            interview_id:
              description: '面试id'
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
            updated_at:
              description: '数据更新时间'
              type: 'string'
            interview_state:
              description: '面试状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, thacher_apponit_sql))


def thacher_apponit_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select t.id,i.id as interview_id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as username,t.mobile,t.email,i.`updated_at`,i.state as interview_state
    from teacher t , interview i  
    where t.`delete_flag` = 'IN_FORCE' and t.state = 'CHECK_PASS' and i.state in(1,6,7,8) and i.teacher_id = t.id  and i.`delete_flag` = 'IN_FORCE' and i.`state` <> 99 
    
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name) like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys():
        sql.append(' and i.state =:state')

    if 'interview_at' in params.keys():
        sql.append(
            ' and i.`start` <:interview_at and i.`end` >:interview_at')
    sql.append(' order by t.id desc')
    return ['id','interview_id', 'username', 'mobile', 'email','updated_at','interview_state'], ''.join(sql)


@manger.route('/interview_result', methods=['POST'])
def interview_result():
    """
    swagger-doc: 'do interview_result query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      teacher_name:
        description: '教师名称'
        type: 'string'
      mobile:
        description: '手机号'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      state:
        description: '0:待填写结果，5：未完成，9：面试通过，10：面试未通过 '
        type: 'string'
      interview_at:
        description: '面试时间 in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      interview_name:
        description: '面试人名称'
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
              description: '教师id'
              type: 'integer'
            interview_id:
              description: '面试id'
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
            updated_at:
              description: '数据更新时间'
              type: 'string'
            interview_state:
              description: '面试状态'
              type: 'string'
            start:
              description: '面试开始时间'
              type: 'string'
            end:
              description: '面试结束时间'
              type: 'string'
            interview_name:
              description: '面试人名称'
              type: 'string'
            interview_state:
              description: '面试状态'
              type: 'string'

    """
    j = request.json
    return jsonify(do_query(j, interview_result_sql))


def interview_result_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
    select t.id,i.id as interview_id,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as username,t.mobile,t.email,i.`start`,i.end,su.name as interview_name,i.state as interview_state
    from teacher t , interview i left join sys_user su on i.`interviewer_id` = su.`id`
    where  t.`delete_flag` = 'IN_FORCE' and t.state = 'WAIT_FOR_INTERVIEW' and i.state in(2,5,9,10) and i.teacher_id = t.id  and i.`delete_flag` = 'IN_FORCE' and i.`state` <> 99 
    ''']

    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name) like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'mobile' in params.keys():
        sql.append(' and t.mobile =:mobile')

    if 'email' in params.keys():
        sql.append(' and t.email =:email')

    if 'state' in params.keys() and params['state'] == '0':
        sql.append(' and i.result is null')

    if 'state' in params.keys() and params['state'] != '0':
        sql.append(' and i.state =:state')

    if 'interview_at' in params.keys():
        sql.append(
            ' and i.`start` <:interview_at and i.`end` >:interview_at')

    if 'interview_name' in params.keys():
        sql.append(" and su.name like '%")
        sql.append(params['interview_name'])
        sql.append("%'")
    sql.append(' order by t.id desc')
    return ['id','interview_id', 'username', 'mobile', 'email','start','end','interview_name','interview_state'], ''.join(sql)


@manger.route('/get_enter_room_url', methods=['POST'])
def get_enter_room_url():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课节id'
        type: 'string'
    res:
      url:
        description: '访问地址'
        type: ''
    """
    course_schedule_id = request.json['course_schedule_id']

    with session_scope(db) as session:

        courseschedule = session.query(CourseSchedule).filter_by(id=course_schedule_id).one_or_none()

        if courseschedule is None :
            return jsonify({
                "error": "not found course_schedule: {0}".format(
                    course_schedule_id)
            }), 500

        courseclassroom = session.query(CourseClassroom).filter_by(course_schedule_id =courseschedule.id).one_or_none()

        if courseclassroom is None :
            return jsonify({
                "error": "found courseclassroom existing in {0}".format(
                    course_schedule_id)
            }), 500

        url = live_service.enter_room(getattr(g, current_app.config['CUR_USER'])['username'],courseclassroom.room_id,getattr(g, current_app.config['CUR_USER'])['nickname'],
                                      ClassroomRoleEnum.ASSISTANT.name,ClassroomDeviceEnum.PC.name)

    return jsonify({'url':url })


@manger.route('/homework', methods=['POST'])
def homework():
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
        description: 'study schedule id 课节id'
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
              description: '作业id'
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
            created_at:
              description: '创建时间'
              type: 'string'
            course_name:
              description: '课程名称'
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
    select hm.id,question_name,homework_type,question_text,question_attachment_url,answer_text,answer_attachment_url,score,score_remark,score_reason,hm.created_at,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,c.course_name,t.avatar as teacher_avatar
    from homework hm,study_schedule sc,course c,teacher t,course_schedule cs
    where 
    hm.study_schedule_id = sc.id and cs.course_id = c.id and c.`primary_teacher_id` = t.id and sc.course_schedule_id = cs.id and hm.homework_type = 1
    and c.state<> 99 
    and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and sc.`delete_flag` = 'IN_FORCE' and hm.`delete_flag` = 'IN_FORCE'  and cs.`delete_flag` = 'IN_FORCE' 
    ''']

    if 'study_schedule_id' in params.keys():
        sql.append(' and sc.id =:study_schedule_id')

    sql.append(' order by hm.id desc')
    current_app.logger.debug(sql)

    return ['id', 'question_name','question_text', 'question_attachment_url', 'created_at'], ''.join(sql)


@manger.route('/view_homework', methods=['POST'])
def view_homework():
    """
    swagger-doc: 'do view_homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      course_schedule_id:
        description: '课程计划ID'
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
              description: '作业id'
              type: 'integer'
            question_name:
              description: '作业名称'
              type: 'string'
            question_text:
              description: '作业'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            question_attachment_url:
              description: '问题附件'
              type: 'string'
            answer_text:
              description: '答案'
              type: 'string'
            answer_attachment_url:
              description: '答案附件'
              type: 'string'
            student_name:
              description: '学生'
              type: 'string'
            score:
              description: '得分'
              type: 'string'
            score_reason:
              description: '得分原因'
              type: 'string'
            review_at:
              description: '点评时间'
              type: 'string'
            evaluation:
              description: '点评'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, view_homework_sql))


def view_homework_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
            select h.id,h.question_name,h.question_text,h.created_at ,h.question_attachment_url,h.answer_text,h.answer_attachment_url,s.name as student_name,h.score,score_reason,h.review_at,ss.teacher_evaluation as evaluation
            from course_schedule cs,homework h,study_schedule ss,student s,course c
            where cs.id = ss.course_schedule_id and ss.id = h.study_schedule_id and ss.student_id = s.id and course_id = c.id and h.homework_type = 2
             and cs.`state` <> 99   and s.`state` <> 99
             and cs.`delete_flag` = 'IN_FORCE' and h.`delete_flag` = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' 
            ''']
    if 'course_schedule_id' in params.keys():
        sql.append(
            ' and cs.id = '+params['course_schedule_id'])
    sql.append(' order by cs.id desc')
    return ['id', 'question_name', 'question_text','created_at','question_attachment_url','answer_text','answer_attachment_url','student_name','score','score_reason','review_at','evaluation'], ''.join(sql)


@manger.route('/student_tryout_apply', methods=['POST'])
def student_tryout_apply():
    """
    swagger-doc: 'do view_homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_name:
        description: '学生名称'
        type: 'string'
      class_at:
        description: '上课时间'
        type: 'string'
      appointment_state:
        description: '状态，枚举值'
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
            course_appointment_id:
              description: '老师试听表id'
              type: 'integer'
            study_appointment_id:
              description: '学生试听表id'
              type: 'string'
            question_text:
              description: '作业'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            apply_by:
              description: '申请人'
              type: 'string'
            student_name:
              description: '学生名称'
              type: 'string'
            open_time_start:
              description: '上课时间'
              type: 'string'
            open_time_end:
              description: '结束时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            appointment_state:
              description: '状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, student_tryout_apply_sql))


def student_tryout_apply_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
      select sa.id as course_appointment_id,sa.id as study_appointment_id,sa.`created_at`,sa.`apply_by`,s.name as student_name,sa.`open_time_start`,sa.`open_time_end`,
      (select t.name from  course_appointment ca, teacher t where ca.teacher_id = t.id and t.`delete_flag` = 'IN_FORCE' and ca.`delete_flag` = 'IN_FORCE' and ca.appointment_state ='ACCEPT' and ca.`study_appointment_id` = sa.id)
      as teacher_name,appointment_state
	 from study_appointment sa, 
	 student s
     where  sa.student_id = s.id and s.`delete_flag` = 'IN_FORCE' and sa.`delete_flag` = 'IN_FORCE'; ''']

    if 'student_name' in params.keys():
        sql.append(" and s.name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'appointment_state' in params.keys():
        sql.append(" and ca.appointment_state =:appointment_state ")

    if 'class_at' in params.keys():
        sql.append(" and sa.open_time_start <=:class_at ")
        sql.append(" and sa.open_time_end >:class_at ")
    sql.append(' order by sa.id desc')
    return ['course_appointment_id', 'study_appointment_id', 'created_at','apply_by','student_name','open_time_start','open_time_end','teacher_name','appointment_state'], ''.join(sql)


@manger.route('/student_tryout_apply_result', methods=['POST'])
def student_tryout_apply_result():
    """
    swagger-doc: 'do view_homework query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      study_appointment_id:
        description: '学生预约id'
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
              description: '教师名称'
              type: 'string'
            mobile:
              description: '电话'
              type: 'string'
            email:
              description: '邮箱'
              type: 'string'
            timezone:
              description: '时区'
              type: 'string'
            appointment_state:
              description: '状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, student_tryout_apply_result_sql))


def student_tryout_apply_result_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
      select ca.id ,concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name,t.mobile,t.email,timezone,ca.appointment_state
	 from  course_appointment ca
	 left join teacher t on ca.teacher_id = t.id and t.`delete_flag` = 'IN_FORCE'
     where ca.`delete_flag` = 'IN_FORCE'  ''']


    sql.append(" and ca.study_appointment_id =:study_appointment_id ")

    sql.append(' order by ca.id desc')
    return ['id', 'teacher_name', 'mobile','email','timezone','appointment_state'], ''.join(sql)


