#!/usr/bin/env python
from filecmp import cmp

from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *

from src.models import db, session_scope,CourseAppointment,StudyAppointment,StudySchedule,CourseClassroom,Homework

from src.services import do_query
import hashlib
from src.services import do_query, datetime_param_sql_format
import json
from src.services import live_service
from src.models import ClassroomRoleEnum, ClassroomDeviceEnum



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
        description: '课程名称'
        type: 'string'
      course_id:
        description: '课程id'
        type: 'string'
      teacher_name:
        description: '教师名称'
        type: 'string'
      course_time:
        description: '上课时间in sql format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      course_status:
        description: '课程状态 1：已上完,2:未上'
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
              description: '课程计划id'
              type: 'integer'
            course_id:
              description: '课程id'
              type: 'string'
            course_name:
              description: '课程名称'
              type: 'string'
            course_desc:
              description: '课程描述'
              type: 'string'
            teacher_avatar:
              description: '教师头像'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            finish:
              description: '已经上完的数量'
              type: 'integer'
            classes_number:
              description: '课节总数'
              type: 'integer'
            start:
              description: '上课开始时间'
              type: 'string'
            end:
              description: '上课结束时间'
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
			select c.id as course_id,c.`course_name`,(select count(*) from study_schedule ss,course_schedule cs  where student_id = o.student_id and course_schedule_id = cs.id  and cs.`delete_flag` = 'IN_FORCE' and cs.course_id = c.id
			and cs.end < now()) as finish,
           c.classes_number,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,c.start,c.end,t.avatar as teacher_avatar,c.course_desc
            from  course c,`order` o, teacher t
            where  o.course_id = c.id and c.primary_teacher_id = t.id  
            and o.`state` <> 99  and c.state<> 99 and o.payment_state in (2,8)
            and o.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE'       
    ''']
    sql.append("and o.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'course_id' in params.keys():
        sql.append(' and c.id =:course_id')

    if 'course_name' in params.keys():
        sql.append(" and (c.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or c.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name)  like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'course_time' in params.keys():
        sql.append(
            ' and c.start <:course_time and c.end >:course_time')
    if 'course_status' in params.keys() and params['course_status'] == '1':
        sql.append(' and c.end <now()')
    if 'course_status' in params.keys() and params['course_status'] == '2':
        sql.append(' and c.end > now()')
    sql.append(' order by c.id desc')

    return ['course_id', 'course_name', 'finish', 'classes_number', 'teacher_name',
            'start', 'end','teacher_avatar','course_desc'], ''.join(sql)


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
        description: '课程名称'
        type: 'string'
      teacher_name:
        description: '教师名称'
        type: 'string'
      order_id:
        description: '订单id'
        type: 'string'
      payment_state:
        description: '支付状态，参考枚举值'
        type: 'string'
      created_at_start:
        description: '上课开始时间 format YYYY-mm-dd HH:MM:ss.SSS'
        type: 'string'
      created_at_end:
        description: '上课结束时间 format YYYY-mm-dd HH:MM:ss.SSS'
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
              description: '订单id'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            classes_number:
              description: '总课节数'
              type: 'integer'
            order_type:
              description: '订单类型参考枚举'
              type: 'integer'
            payment_state:
              description: '支付状态'
              type: 'string'
            created_at:
              description: '订单创建时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            order_amount:
              description: '订单金额'
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
    o.`payment_state`,o.`created_at`,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,o.`amount`
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
        sql.append(" and (c.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or c.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'teacher_name' in params.keys():
        sql.append(" and concat(t.first_name,' ',t.middle_name,' ',t.last_name)  like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'payment_state' in params.keys():
        sql.append(' and o.payment_state = :payment_state')
    if 'created_at_start' in params.keys() \
            and 'created_at_end' in params.keys():
        sql.append(
            ' and o.created_at between :created_at_start and '
            ':created_at_end')
    sql.append(' order by o.id desc')
    return ['id', 'course_name', 'classes_number', 'order_type',
            'payment_state','created_at', 'teacher_name', 'amount'], ''.join(sql)


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
        description: 'study schedule id 课节id'
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
              description: '作业id'
              type: 'integer'
            homework_type:
              description: '作业类型，参考常量'
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
              description: '创建时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            teacher_avatar:
              description: '教师头像'
              type: 'string'
            course_name:
              description: '课程名称'
              type: 'string'
            teacher_evaluation:
              description: '教师评价'
              type: 'string'
            name:
              description: '课节名称'
              type: 'string'
            student_evaluation:
              description: '老师给学生的评价'
              type: 'string'
            evaluation:
              description: '评价'
              type: 'string'
            name:
              description: '课节名称'
              type: 'string'
            study_schedule_id:
              description: '课节id'
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
    select hm.id,question_name,homework_type,question_text,question_attachment_url,answer_text,answer_attachment_url,score,score_remark,score_reason,hm.created_at,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,c.course_name_zh as course_name,
    t.avatar as teacher_avatar,sc.teacher_evaluation,cs.name,sc.student_evaluation,hm.evaluation,sc.name,sc.id as study_schedule_id 
	from study_schedule sc ,course_schedule cs,homework hm ,course c,teacher t
	where sc.course_schedule_id = cs.id and cs.id = hm.course_schedule_id and cs.course_id = c.id  and c.`primary_teacher_id` = t.id
	and c.state<> 99 
    and t.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and sc.`delete_flag` = 'IN_FORCE' and hm.`delete_flag` = 'IN_FORCE'  and cs.`delete_flag` = 'IN_FORCE'  
    ''']
    sql.append(
        " and sc.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'study_schedule_id' in params.keys():
        sql.append(' and sc.id =:study_schedule_id')

    if 'homework_state' in params.keys() \
             and params['homework_state']== '1':
        sql.append(' and hm.homework_id is not null and hm.homework_type = 2')

    if 'homework_state' in params.keys() \
             and params['homework_state'] == '2':
        sql.append('  and hm.homework_type = 1 and hm.id  not in ( select he1.homework_id from homework he1,study_schedule sc1 '
                   'where homework_type = 2 and he1.`study_schedule_id` = sc1.id and sc1.`student_id` ='
                   + getattr(g, current_app.config['CUR_USER'])['id']+')')
    sql.append(' order by hm.id desc')
    current_app.logger.debug(sql)

    return ['id', 'question_name', 'homework_type', 'question_text', 'question_attachment_url',
            'answer_text', 'answer_attachment_url', 'score', 'score_remark', 'score_reason', 'created_at',
            'teacher_name','course_name','teacher_avatar','teacher_evaluation','name','student_evaluation','evaluation','name','study_schedule_id'], ''.join(sql)


@student.route('/report_card', methods=['POST'])
def report_card():
    """
    swagger-doc: 'do mreport_card query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_id:
        description: '学生id，如果不传认为是自己'
        type: 'string'
      course_id:
        description: '课程id'
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
              description: '学习结果id'
              type: 'integer'
            course_id:
              description: '课程id'
              type: 'string'
            course_name:
              description: '课程名称'
              type: 'string'
            created_at:
              description: '创建时间'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            report_card_url:
              description: '成绩单地址'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, report_card_sql))


def report_card_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
	select sr.id,c.id as course_id,c.`course_name`,sr.`created_at`,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,sr.report_card_url
	from study_result sr,course_exam ce,course c,teacher t
	where sr.course_exam_id = ce.id and ce.course_id = c.id and c.primary_teacher_id = t.id
    and ce.state<> 99 and c.`state` <> 99  and t.state<> 99 
    and sr.`delete_flag` = 'IN_FORCE' and ce.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and t.`delete_flag` = 'IN_FORCE'  
    ''']

    if 'student_id' in params.keys():
        sql.append(" and sr.student_id =:student_id")
    else:
        sql.append(" and sr.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'course_id' in params.keys():
        sql.append(' and c.id =:course_id')
    sql.append(' order by sr.id desc')
    return ['id', 'course_id', 'course_name', 'created_at', 'teacher_name','report_card_url'], ''.join(sql)


@student.route('/schedule', methods=['POST'])
def student_schedule():
    """
    swagger-doc: 'do mreport_card query'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      student_id:
        description: '学生id，如果不传认为是自己'
        type: 'string'
      course_id:
        description: '课程id'
        type: 'string'
      course_schedule_id:
        description: '课程计划id'
        type: 'string'
      course_schedule_state:
        description: '课程状态，1：已经上课，2；未上'
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
              description: '课节id'
              type: 'integer'
            name:
              description: '课节名称'
              type: 'string'
            start:
              description: '上课开始时间'
              type: 'string'
            end:
              description: '上课结束时间'
              type: 'string'
            courseware_num:
              description: '课件数量,0:未上传，>0已经上传'
              type: 'integer'
            course_id:
              description: ''
              type: 'integer'
    """
    j = request.json
    return jsonify(do_query(j, student_schedule_sql))


def student_schedule_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
        select sr.id,sr.name,actual_start as start,actual_end as end,cs1.`course_id`,
        (select count(*) from course c1,courseware cs where c1.`id` = cs.`course_id` and c1.id = cs1.course_id and c1.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE') as courseware_num
        from study_schedule sr,course_schedule cs1
        where cs1.id = sr.course_schedule_id
        and cs1.`state` <> 99  
        and sr.`delete_flag` = 'IN_FORCE' and cs1.`delete_flag` = 'IN_FORCE'
    ''']

    if 'student_id' in params.keys():
        sql.append(" and sr.student_id =:student_id")
    else:
        sql.append(" and sr.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'course_id' in params.keys():
        sql.append(' and cs1.course_id =:course_id')
    if 'course_schedule_id' in params.keys():
            sql.append(' and cs1.id =:course_schedule_id')

    if 'course_schedule_state' in params.keys() and '1'==params['course_schedule_state']:
        sql.append(' and cs1.end < now()')

    if 'course_schedule_state' in params.keys() and '2'==params['course_schedule_state']:
        sql.append(' and cs1.end >= now()')
    sql.append(' order by sr.id desc')
    return ['id', 'name', 'start', 'end','course_id', 'courseware_num'], ''.join(sql)


@student.route('/growth_report', methods=['POST'])
def growth_report():
    """
    swagger-doc: 'do growth_reportquery'
    required: []
    req:
      page_limit:
        description: 'records in one page'
        type: 'integer'
      page_no:
        description: 'page no'
        type: 'integer'
      study_schedule_id:
        description: '课节id'
        type: 'string'
      course_id:
        description: '课程id'
        type: 'string'
      course_name:
        description: '课程包名'
        type: 'string'
      class_at:
        description: '上课时间'
        type: 'string'
      class_name:
        description: '课程名称'
        type: 'string'
      teacher_name:
        description: '教师名称'
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
              description: '根据type类别判定：type=schedulec此时id=study_schedule_id,type=result此时id=study_result_id'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            course_name_zh:
              description: '课程名称'
              type: 'string'
            teacher_name:
              description: '教师名称'
              type: 'string'
            clasee_name:
              description: '课节名称'
              type: 'string'
            evaluation:
              description: '评价内容，json'
              type: 'string'
            report_card_url:
              description: '成绩单地址'
              type: 'string'
            type:
              description: '类别'
              type: 'string'
            result_type:
              description: '结果类别，NO:课程，SUMMARY：总结，ACHIEVEMENT：成绩单'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, growth_report_sql))


def growth_report_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''''']

    sql.append(" select * from (")
    sql.append(" select sr.id ,c.`course_name` as course_name,c.`course_name_zh` as course_name_zh,sr.name as class_name,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,sr.`created_at`,sr.teacher_evaluation as evaluation, '' as report_card_url,'schedule' as 'type','NO' as 'result_type',c.start,c.end,sr.id as study_schedule_id "
               "from study_schedule sr,course_schedule cs,course c ,teacher t "
               "where cs.id = sr.course_schedule_id and cs.course_id = c.id and c.`primary_teacher_id` = t.id "
               "and cs.`state` <> 99  and c.`state` <> 99  and sr.teacher_evaluation is not null "
               "and sr.`delete_flag` = 'IN_FORCE' and cs.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE'")
    sql.append(" and sr.student_id = "+ getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_id' in params.keys():
        sql.append(" and c.id =:course_id")
    sql.append(" union all ")
    sql.append(" select sr.id, c.`course_name` as course_name,c.`course_name_zh` as course_name_zh,'NO' as class_name,concat(t.first_name,' ',t.middle_name,' ',t.last_name)  as teacher_name,sr.`created_at`,sr.evaluation,sr.report_card_url,'result' as 'type',sr.result_type,c.start,c.end,'0' as study_schedule_id "
               "from study_result sr,course c ,teacher t "
               "where sr.course_id = c.id and c.`primary_teacher_id` = t.id "
               "and c.`state` <> 99  and sr.`delete_flag` = 'IN_FORCE' "
               "and c.`delete_flag` = 'IN_FORCE'")
    sql.append(" and sr.student_id = "+ getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_id' in params.keys():
        sql.append(" and c.id =:course_id")
    sql.append(" ) t  where 1=1")

    if 'study_schedule_id' in params.keys():
        sql.append(" and t.study_schedule_id =:study_schedule_id")
    if 'course_name' in params.keys():
        sql.append(" and (t.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or t.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'teacher_name' in params.keys():
        sql.append(" and t.teacher_name like '%")
        sql.append(params['teacher_name'])
        sql.append("%'")
    if 'class_name' in params.keys():
        sql.append(" and t.class_name like '%")
        sql.append(params['class_name'])
        sql.append("%'")

    if 'created_at' in params.keys():
        sql.append(" and t.start <:created_at and t.end <:created_at")

    sql.append(" order by t.id desc")

    return ['id', 'course_name', 'course_name_zh','class_name','teacher_name', 'created_at', 'evaluation','report_card_url','type','result_type','start','end'], ''.join(sql)


@student.route('/subject', methods=['POST'])
def my_subject():
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
      type:
        description: '科目类别'
        type: 'string'
      student_id:
        description: '学生id，不传默认自己'
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
              description: 'student_subject_id'
              type: 'integer'
            subject_id:
              description: 'subject_id'
              type: 'integer'
            subject_category_id:
              description: 'subject_category_id'
              type: 'integer'
            curriculum_id:
              description: 'curriculum_id'
              type: 'integer'
            subject_name:
              description: '名称'
              type: 'string'
            type:
              description: '类型'
              type: 'integer'
            subject_name_zh:
              description: '三级中文名字'
              type: 'integer'
            subject_category_zh:
              description: '二级中文名字'
              type: 'string'
            full_name_zh:
              description: '一级中文名字'
              type: 'integer'

    """
    j = request.json
    return jsonify(do_query(j, my_subject_sql))


def my_subject_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
          select th.id,th.`subject_id`,su.subject_name_zh,sc.id as subject_category_id,sc.subject_category_zh,cu.id as curriculum_id,cu.full_name_zh,th.subject_name,th.subject_type as type
          from student_subject th  left join subject su on th.`subject_id` = su.id and su.state <> 99 and su.`delete_flag` = 'IN_FORCE'
          left join subject_category sc on su.`subject_category_id` = sc.id and sc.state <> 99 and sc.`delete_flag` = 'IN_FORCE'
          left join curriculum cu on sc.`curriculum_id` = cu.id and cu.state <> 99 and cu.`delete_flag` = 'IN_FORCE'
          where th.`delete_flag` = 'IN_FORCE'
            ''']

    if 'type' in params.keys():
        sql.append(' and th.subject_type =:type ')
    if 'teacher_id' in params.keys():
        sql.append(' and th.student_id =:student_id ')
    else:
        sql.append("and th.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    sql.append(' order by th.id desc')

    return ['id', 'subject_id','subject_name_zh', 'subject_category_id','subject_category_zh','curriculum_id','full_name_zh','subject_name','type'], ''.join(sql)


@student.route('/apply_tryout', methods=['POST'])
def apply_tryout():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      start:
        description: '开始时间'
        type: 'string'
      end:
        description: '结束时间'
        type: 'string'
      student_id:
        description: '学生id，不传默认自己'
        type: 'string'

    res:
      verify_code:
        description: 'id'
        type: ''
    """
    start = request.json['start'].replace('T', ' ').replace('Z', '')
    end = request.json['end'].replace('T', ' ').replace('Z', '')
    student_id =  getattr(g, current_app.config['CUR_USER'])['id']
    if 'student_id' in request.json:
        student_id = request.json['student_id']

    with session_scope(db) as session:

        studyAppointment = StudyAppointment(
            student_id = student_id,
            delete_flag = 'IN_FORCE',
            open_time_start= start,
            open_time_end = end,
            appointment_state='WRITE_APPOINTMENT',
            updated_by=getattr(g, current_app.config['CUR_USER'])['username'],
            apply_by=getattr(g, current_app.config['CUR_USER'])['username']
        )

        session.add(studyAppointment)
        session.flush()

    return jsonify({'id':studyAppointment.id })


@student.route('/get_preview_doc', methods=['POST'])
def get_preview_doc():
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
      study_schedule_id:
        description: '课节id'
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
            ware_uid:
              description: '课件url，多贝'
              type: 'string'


    """
    j = request.json
    return jsonify(do_query(j, get_preview_doc_sql))


def get_preview_doc_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
           select cw.`ware_uid`
           from study_schedule ss , courseware cw
           where ss.course_schedule_id = cw.course_schedule_id  and ss.`delete_flag` = 'IN_FORCE'  and cw .`delete_flag` = 'IN_FORCE'
            ''']


    sql.append(' and ss.id =:study_schedule_id ')
    sql.append("and ss.student_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    sql.append(' order by ss.id desc')

    return ['ware_uid'], ''.join(sql)


@student.route('/get_enter_room_url', methods=['POST'])
def get_enter_room_url():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      study_schedule_id:
        description: '课节id'
        type: 'string'
    res:
      url:
        description: '登录地址'
        type: ''
    """
    study_schedule_id = request.json['study_schedule_id']

    with session_scope(db) as session:

        studyschedule = session.query(StudySchedule).filter_by(id=study_schedule_id).one_or_none()

        if studyschedule is None :
            return jsonify({
                "error": "not found Study_Schedule: {0}".format(
                    study_schedule_id)
            }), 500
        current_app.logger.debug('studyschedule.schedule_type-------------'+studyschedule.schedule_type)
        if studyschedule.schedule_type == 'LOCKED' :
            return jsonify({
                "error": "study schedule has locked"
            }), 500


        courseclassroom = session.query(CourseClassroom).filter_by(course_schedule_id =studyschedule.course_schedule_id).one_or_none()

        if courseclassroom is None :
            return jsonify({
                "error": "found courseclassroom existing in {0}".format(
                    study_schedule_id)
            }), 500

        url = live_service.enter_room(getattr(g, current_app.config['CUR_USER'])['username'],courseclassroom.room_id,getattr(g, current_app.config['CUR_USER'])['nickname'],
                                      ClassroomRoleEnum.STUDENT.name,ClassroomDeviceEnum.PC.name)

    return jsonify({'url':url })


@student.route('/write_homework', methods=['POST'])
def write_homework():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      study_schedule_id:
        description: '课节id'
        type: 'string'
      title:
        description: '标题'
        type: 'string'
      desc:
        description: '描述'
        type: 'string'
      attachment:
        description: '附件，可以考虑JSON地址'
        type: 'string'
      homework_id:
        description: '作业id'
        type: 'string'
    res:
      id:
        description: ''
        type: ''
    """
    study_schedule_id = request.json['study_schedule_id']
    homework_id = request.json['homework_id']
    attachment = ''
    title = ''
    desc =''
    if 'attachment' in request.json:
        attachment = request.json['attachment']
    if 'title' in request.json:
        title = request.json['title']
    if 'desc' in request.json:
        desc = request.json['desc']

    with session_scope(db) as session:


        homework = session.query(Homework).filter_by(id=homework_id).one_or_none()

        if homework is None :
            return jsonify({
                "error": "not found homework: {0}".format(
                    homework_id)
            }), 500

        studyschedule = session.query(StudySchedule).filter_by(id=study_schedule_id).one_or_none()

        if studyschedule is None :
            return jsonify({
                "error": "not found Study_Schedule: {0}".format(
                    study_schedule_id)
            }), 500

        homework1 = Homework(homework_type = 2,
                            answer_text = desc,
                            answer_attachment_url = attachment,
                            study_schedule_id = studyschedule.id,
                            homework_id = homework_id,
                            question_name = title,
                            delete_flag = 'IN_FORCE',
                            course_schedule_id = homework.course_schedule_id,
                            updated_by=getattr(g, current_app.config['CUR_USER'])['username']

                            )
        session.add(homework1)
        session.flush()

    return jsonify({'id':homework.id })


@student.route('/get_courseware', methods=['POST'])
def get_courseware():
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
      study_schedule_id:
        description: '课节id'
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
            ware_uid:
              description: '课件url，多贝'
              type: 'string'
            name:
              description: '课节名称'
              type: 'string'
            start:
              description: '上课时间'
              type: 'string'
            end:
              description: '上课结束时间'
              type: 'string'
            ware_name:
              description: '课件名称'
              type: 'string'
            ware_url:
              description: '课件地址'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, get_courseware_sql))


def get_courseware_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
           select cw.`ware_uid`,ss.`name` ,ss.actual_start as start,ss.actual_end as end,cw.`ware_name`,cw.ware_url
           from study_schedule ss, courseware cw
           where ss.course_schedule_id = cw.course_schedule_id and cw .`delete_flag` = 'IN_FORCE' and ss .`delete_flag` = 'IN_FORCE'
         ''']

    sql.append(' and ss.id =:study_schedule_id ')

    sql.append(' order by ss.id desc')

    return ['ware_uid','name','start','end','ware_name','ware_url'], ''.join(sql)

