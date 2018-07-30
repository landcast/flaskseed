#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime,time

from sqlalchemy.sql import *

from src.models import db, session_scope,Teacher,Interview,TeacherState, \
    CourseAppointment,StudySchedule,Homework,CourseSchedule,CourseClassroom,StudyAppointment,\
    Course,Order,PayLog,ClassroomTypeEnum
from src.services import do_query, datetime_param_sql_format
from src.utils import generate_pdf_from_template
import uuid
from src.services import live_service
from src.models import ClassroomRoleEnum, ClassroomDeviceEnum

teacher = Blueprint('teacher', __name__)


@teacher.route('/main_query', methods=['POST'])
def teacher_query():
    """
    swagger-doc: 'do teacher query'
    required: []
    req:
      page_limit:
        description: 'records in one page 分页中每页条数'
        type: 'integer'
      page_no:
        description: 'page no, start from 1 分页中页序号'
        type: 'integer'
      category_1:
        description: '一级分类id'
        type: 'string'
      category_2:
        description: '二级分类id'
        type: 'string'
      category_3:
        description: '三级分类id'
        type: 'string'
      cur_category_1:
        description: '当前教学一级分类id'
        type: 'string'
      cur_category_2:
        description: '当前教学二级分类id'
        type: 'string'
      cur_category_3:
        description: '当前教学三级分类id'
        type: 'string'
      username:
        description: '教师名称'
        type: 'string'
      mobile:
        description: '电话'
        type: 'string'
      email:
        description: '邮箱'
        type: 'string'
      country:
        description: '国家'
        type: 'string'
      province:
        description: '省/州'
        type: 'string'
      timezone:
        description: '时区'
        type: 'string'
      school:
        description: '学校'
        type: 'string'
      cur_grade:
        description: '当前教授年级'
        type: 'string'
      cur_province:
        description: '当前州/省'
        type: 'string'
      cur_area:
        description: '当前任职地区'
        type: 'string'
      grade:
        description: '可以教授年级'
        type: 'string'
      teacher_age:
        description: '总教龄0-4，5-9，10-15等'
        type: 'string'
      have_award:
        description: '是否有奖励0：无，1：有'
        type: 'string'
      have_seniority:
        description: '是否有资格证明0：无，1：有'
        type: 'string'
      week:
        description: '可上课周'
        type: 'string'
      start:
        description: '选择起始时间，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      end:
        description: '选择结束时间，格式： YYYY-mm-ddTHH:MM:ss.SSSZ'
        type: 'string'
      state:
        description: '81，不在岗，80：在岗'
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
            created_at:
              description: '注册时间'
              type: 'string'
            username:
              description: '教师账号'
              type: 'integer'
            mobile:
              description: '手机'
              type: 'integer'
            email:
              description: '邮箱'
              type: 'integer'
            country:
              description: '国家'
              type: 'string'
            province:
              description: '州，省'
              type: 'string'
            timezone:
              description: '时区'
              type: 'string'
            state:
              description: '教师状态'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(
        datetime_param_sql_format(j, ['start', 'end']),
        teacher_query_sql))


def teacher_query_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    sql = ['''
        select t.id,t.`created_at`,t.`username`,t.`mobile`,t.`email`,t.country,t.`province`,t.timezone,t.`state` 
        from teacher t 
        left join teacher_history th on t.id = th.`teacher_id` and th.`delete_flag` = 'IN_FORCE'
        left join subject s on th.`subject_id` = s.id and s.`delete_flag` = 'IN_FORCE' 
        left join subject_category sc on s.`subject_category_id` = sc.id and sc.`delete_flag` = 'IN_FORCE'
        left join curriculum cr on sc.`curriculum_id` = cr.id and cr.`delete_flag` = 'IN_FORCE'  
        left join teacher_time tt on t.id = tt.`teacher_id` and tt.`delete_flag` = 'IN_FORCE'
        where t.`delete_flag` = 'IN_FORCE'
    ''']
    if 'username' in params.keys():
        sql.append(' and t.username = :username')
    if 'mobile' in params.keys():
        sql.append(' and t.mobile = :mobile')
    if 'email' in params.keys():
        sql.append(' and t.email = :email')
    if 'country' in params.keys():
        sql.append(' and t.country = :country')
    if 'province' in params.keys():
        sql.append(' and t.province = :province')

    if 'timezone' in params.keys():
        sql.append(' and t.timezone = :timezone')
    if 'school' in params.keys():
        sql.append(" and t.cur_school like '%")
        sql.append(params['school'])
        sql.append("%'")
    if 'cur_grade' in params.keys():
        sql.append(" and t.cur_grade like '%")
        sql.append(params['cur_grade'])
        sql.append("%'")

    if 'cur_province' in params.keys():
        sql.append(' and t.cur_province = :cur_province')

    if 'cur_area' in params.keys():
        sql.append(' and t.cur_area = :cur_area')

    if 'grade' in params.keys():
        sql.append(" and th.grade like '%")
        sql.append(params['grade'])
        sql.append("%'")

    if 'teacher_age' in params.keys() and '-' in 'teacher_age':
        sql.append(' and t.teacher_age >')
        sql.append(params['teacher_age'].split('-')[0])
        sql.append(' and t.teacher_age <')
        sql.append(params['teacher_age'].split('-')[1])

    if 'have_award' in params.keys() and params['have_award'] == '0':
        sql.append(' and t.award_url is null')

    if 'have_award' in params.keys() and params['have_award'] == '1':
        sql.append(' and t.award_url is not null')

    if 'have_seniority' in params.keys() and params['have_seniority'] == '0':
        sql.append(' and t.seniority_url is null')

    if 'have_seniority' in params.keys() and params['have_seniority'] == '1':
        sql.append(' and t.seniority_url is not null')

    if 'week' in params.keys():
        sql.append(' and tt.week = :week')

    if 'start' in params.keys() \
            and 'end' in params.keys():
        sql.append(' and ((tt.start >:start and tt.end<:start) or (tt.start >:end and tt.end<:end))')

    if 'state' in params.keys():
        sql.append(' and t.state  =:state')

    if 'category_1' in params.keys():
        sql.append(' and cr.id =:category_1 and th.type = 1')
    if 'category_2' in params.keys():
        sql.append(' and sc.id =:category_2 and th.type = 1')
    if 'category_3' in params.keys():
        sql.append(' and s.id =:category_3 and th.type = 1')
    if 'cur_category_1' in params.keys():
        sql.append(' and cr.id =:cur_category_1 and th.type = 2')
    if 'cur_category_2' in params.keys():
        sql.append(' and sc.id =:cur_category_2 and th.type = 2')
    if 'cur_category_3' in params.keys():
        sql.append(' and s.id =:category_3 and th.type = 2')

    # current_app.logger.debug(sql)
    return ['id', 'created_at', 'username', 'mobile', 'email',
            'country', 'province', 'timezone', 'state'], ''.join(sql)


@teacher.route('/check_pass', methods=['POST'])
def refund():
    """
    swagger-doc: 'refund'
    required: []
    req:
      teacher_id:
        description: '教师id'
        type: 'string'
    res:
      id:
        description: 'id'
        type: 'string'
    """
    teacher_id = request.json['teacher_id']


    with session_scope(db) as session:

        teacher = session.query(Teacher).filter_by(id=teacher_id).one_or_none()

        if teacher is None:
            return jsonify({
                "error": "not found teacher_id:{0} ".format(
                    teacher_id)
            }), 500

        setattr(teacher,'state',TeacherState.CHECK_PASS.name)

        session.add(teacher)

        interview = Interview(state = 1,
                         delete_flag = 'IN_FORCE',
                         updated_by=getattr(g, current_app.config['CUR_USER'])['username'],
                         interviewer_id =getattr(g, current_app.config['CUR_USER'])['id'],
                         teacher_id = teacher_id
                )
        session.add(interview)

    return jsonify({'id':interview.id })


@teacher.route('/contract', methods=['POST'])
def content_file():
    """
    swagger-doc: 'refund'
    required: []
    req:
      teacher_id:
        description: '教师id'
        type: 'string'
      salary:
        description: '金额'
        type: 'string'
      date:
        description: '日期'
        type: 'string'
    res:
      download_file:
        description: '下载地址'
        type: 'string'
    """
    teacher_id = request.json['teacher_id']
    salary = request.json['salary']
    date = request.json['date']

    with session_scope(db) as session:

        teacher = session.query(Teacher).filter_by(
            id=teacher_id).one_or_none()

        if teacher is None:
            return jsonify({
                "error": "not found teacher_id:{0} ".format(
                    teacher_id)
            }), 500

        param_dict = {
            'teacher_name': teacher.username,
            'effective_date': salary,
            'teacher_salary': date
        }

        file = str(uuid.uuid1())+'.pdf'

        status, output = generate_pdf_from_template('agreement.html',
                                                    param_dict, './src/static/contract/'+file)

        result = []

        result.append({'download_file': '/static/contract/'+file})

        setattr(teacher,'contract_url','/static/contract/'+file)

        session.add(teacher)

        session.flush()

    return jsonify(result)


@teacher.route('/create_homework', methods=['POST'])
def teacher_homework():
    """
    swagger-doc: 'refund'
    required: []
    req:
      course_schedule_id:
        description: '课程计划id'
        type: 'string'
      title:
        description: '标题'
        type: 'string'
      desc:
        description: '描述'
        type: 'string'
      attachment_url:
        description: '附件地址'
        type: 'string'
    res:
      id:
        description: '下载地址'
        type: 'string'
    """
    course_schedule_id = request.json['course_schedule_id']
    title = request.json['title']
    desc = request.json['desc']
    attachment_url = ''

    if 'attachment_url' in request.json :
        attachment_url = request.json['attachment_url']

    with session_scope(db) as session:

        courseschedule = session.query(CourseSchedule).filter_by(
            id=course_schedule_id).one_or_none()

        if courseschedule is None:
            return jsonify({
                "error": "not found course_schedule_id:{0} ".format(
                    course_schedule_id)
            }), 500

        studyschedules = session.query(StudySchedule).filter_by(course_schedule_id=courseschedule.id)

        for studyschedule in studyschedules:

            homework = Homework(
                homework_type = 1,
                question_name= title,
                question_text= desc,
                question_attachment_url=attachment_url,
                study_schedule_id = studyschedule.id
            )

            session.add(homework)

            session.flush()

    return jsonify({'id':homework.id })


@teacher.route('/my_course', methods=['POST'])
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
      course_id:
        description: '课程id'
        type: 'string'
      course_name:
        description: '课程名称'
        type: 'string'
      student_name:
        description: '学生名称'
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
              description: '课程id'
              type: 'integer'
            course_name:
              description: '课程名称'
              type: 'string'
            course_name_zh:
              description: '课程名称'
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
            student_name:
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
          select * from(
            select 
            	c.id,c.course_name,c.course_name_zh,c.classes_number,c.start,c.end,
            	(select GROUP_CONCAT(s.username) from study_schedule ss,student s,course_schedule cs  where ss.student_id = s.id and ss.course_schedule_id = cs.id and c.`id` = cs.course_id 
            	and cs.`delete_flag` = 'IN_FORCE' and cs.state <> 99  and s.`delete_flag` = 'IN_FORCE' and s.state <> 99 and ss.`delete_flag` = 'IN_FORCE' ) as student_name,
            	(select count(*) from course_schedule where c.`id` = course_id and end < now() ) as finish
            from  course c
            where  c.state<> 99 and c.`delete_flag` = 'IN_FORCE' 
            ''']
    sql.append("and c.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    sql.append(" ) t where 1=1 ")

    if 'course_name' in params.keys():
        sql.append(" and (t.course_name like '%")
        sql.append(params['course_name'])
        sql.append("%'")
        sql.append(" or t.course_name_zh like '%")
        sql.append(params['course_name'])
        sql.append("%')")
    if 'student_name' in params.keys():
        sql.append(" and t.student_name like '%")
        sql.append(params['student_name'])
        sql.append("%'")
    if 'course_time' in params.keys():
        sql.append(
            ' and t.start <:course_time and t.end >:course_time')
    if 'course_id' in params.keys():
        sql.append(
            ' and t.id=:course_id')
    if 'course_status' in params.keys() \
            and params['course_status'] == '1':
        sql.append(' and t.end <now()')
    if 'course_status' in params.keys() \
            and params['course_status'] == '2':
        sql.append(' and t.end > now()')

    return ['id', 'course_name', 'course_name_zh','classes_number', 'start', 'end',
            'student_name', 'finish'], ''.join(sql)


@teacher.route('/my_homework', methods=['POST'])
def my_homework():
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
          select h.id,h.question_name,h.question_text,h.created_at from 
          course_schedule cs,homework h,study_schedule ss,course c
            where cs.id = ss.course_schedule_id and ss.id = h.study_schedule_id and course_id = c.id
             and cs.`state` <> 99   
             and cs.`delete_flag` = 'IN_FORCE' and h.`delete_flag` = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE'  and c.`delete_flag` = 'IN_FORCE' 
            ''']

    sql.append(
        " and c.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'course_schedule_id' in params.keys():
        sql.append(
            ' and cs.id = '+params['course_schedule_id'])

    sql.append(' group by h.question_name')

    return ['id', 'question_name', 'question_text','created_at'], ''.join(sql)


@teacher.route('/view_homework', methods=['POST'])
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
          select h.id,h.question_name,h.question_text,h.created_at ,h.question_attachment_url,h.answer_text,h.answer_attachment_url,s.username as student_name,h.score,score_reason,h.review_at
			from course_schedule cs,homework h,study_schedule ss,student s,course c
            where cs.id = ss.course_schedule_id and ss.id = h.study_schedule_id and ss.student_id = s.id and course_id = c.id
             and cs.`state` <> 99   and s.`state` <> 99
             and cs.`delete_flag` = 'IN_FORCE' and h.`delete_flag` = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' 
            ''']
    sql.append(
        " and c.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_schedule_id' in params.keys():
        sql.append(
            ' and cs.id = '+params['course_schedule_id'])

    return ['id', 'question_name', 'question_text','created_at','question_attachment_url','answer_text','answer_attachment_url','student_name','score','score_reason','review_at'], ''.join(sql)


@teacher.route('/my_course_on', methods=['POST'])
def my_course_on():
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
      course_id:
        description: '课程ID'
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
              description: '课节id course_schedule_id'
              type: 'integer'
            name:
              description: '课节名称'
              type: 'string'
            start:
              description: '上课时间'
              type: 'string'
            end:
              description: '下课时间'
              type: 'string'
            class_type:
              description: '课程类型'
              type: 'integer'

    """
    j = request.json
    return jsonify(do_query(j, my_course_on_sql))


def my_course_on_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
          select cs.id,cs.name,c.class_type,cs.start,cs.end from 
            course_schedule cs,course c
            where cs.`state` <> 99 and cs.course_id = c.id 
             and cs.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE'
             and cs.end < now()
            ''']
    sql.append("and c.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    if 'course_id' in params.keys():
        sql.append(
            ' and c.id = '+params['course_id'])

    return ['id', 'name', 'class_type','start', 'end'], ''.join(sql)


@teacher.route('/my_course_off', methods=['POST'])
def my_course_off():
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
      course_id:
        description: '课程ID'
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
              description: '课节id course_schedule_id'
              type: 'integer'
            courseware_id:
              description: '课件id course_schedule_id'
              type: 'integer'
            name:
              description: '课节名称'
              type: 'string'
            start:
              description: '上课时间'
              type: 'string'
            end:
              description: '下课时间'
              type: 'string'
            checked_result:
              description: '课件审核状态'
              type: 'string'
            ware_url:
              description: '课件地址'
              type: 'string'
            ware_uid:
              description: '多贝课件预览地址'
              type: 'string'

    """
    j = request.json
    return jsonify(do_query(j, my_course_off_sql))


def my_course_off_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
          select cs.id,c.id as courseware_id,cs.name,cs.start,cs.end,c.checked_result,c.ware_url,c.ware_uid from 
            course_schedule cs,courseware c,course cou
            where cs.`state` <> 99  and cs.course_id = cou.id 
             and cs.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' and cou.`delete_flag` = 'IN_FORCE'
             and cs.end > now()
            ''']
    sql.append("and cou.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    if 'course_id' in params.keys():
        sql.append(
            ' and c.id = '+params['course_id'])

    return ['id','courseware_id' ,'name','start', 'end','checked_result','ware_url','ware_uid'], ''.join(sql)


@teacher.route('/my_course_result', methods=['POST'])
def my_course_result():
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
      course_id:
        description: '课程ID'
        type: 'string'
      type:
        description: 'SUMMARY:总结 ACHIEVEMENT：成绩单'
        type: 'string'
    res:
      num_results:
        description: 'SUMMARY/ACHIEVEMENT'
        type: 'string'
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
              description: '课程结果id'
              type: 'integer'
            student_name:
              description: '学生名称'
              type: 'string'
            start:
              description: '评价开始时间'
              type: 'string'
            end:
              description: '评价结束时间'
              type: 'string'
            report_card_name:
              description: '成绩单名称'
              type: 'string'
            report_card_url:
              description: '成绩单地址'
              type: 'string'
    """
    j = request.json
    return jsonify(do_query(j, my_course_result_sql))


def my_course_result_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
          select sr.id,s.username student_name,ce.`start`,ce.end,sr.report_card_name,sr.report_card_url
			from study_result sr,course_exam ce,student s,course c
            where sr.course_exam_id = ce.id and sr.student_id = s.id and ce.course_id = c.id
             and ce.`state` <> 99   and s.`state` <> 99 and c.`state` <> 99
             and sr.`delete_flag` = 'IN_FORCE'  and ce.`delete_flag` = 'IN_FORCE' and s.`delete_flag` = 'IN_FORCE' and c.`delete_flag` = 'IN_FORCE' 
            ''']
    sql.append("and c.primary_teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])

    sql.append(' and sr.result_type =:type')

    if 'course_id' in params.keys():
        sql.append(
            ' and c.id = '+params['course_id'])

    return ['id','student_name' ,'start', 'end','report_card_name','report_card_url'], ''.join(sql)


@teacher.route('/upload_courseware', methods=['POST'])
def upload_courseware():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课节id'
        type: 'string'
      file_url:
        description: '上传服务器后返回的地址'
        type: 'string'
      ware_name:
        description: '课件名称'
        type: 'string'
      is_view:
        description: '是否可看'
        type: 'string，YES/NO'
    res:
      verify_code:
        description: 'id'
        type: ''
    """
    course_schedule_id = request.json['course_schedule_id']
    file_url = request.json['file_url']
    ware_name = request.json['ware_name']
    is_view = request.json['is_view']

    with session_scope(db) as session:

        courseSchedule = session.query(CourseSchedule).filter_by(id=course_schedule_id).one_or_none()

        if courseSchedule is None :
            return jsonify({
                "error": "not found course_schedule: {0}".format(
                    course_schedule_id)
            }), 500

        courseClassroom = session.query(CourseClassroom).filter_by(course_schedule_id=course_schedule_id).one_or_none()

        if courseClassroom is None :
            return jsonify({
                "error": "not found Course_Class_room: {0}".format(
                    course_schedule_id)
            }), 500

        live_service.upload_doc(getattr(g, current_app.config['CUR_USER'])['username'],file_url,ware_name,courseSchedule.course_id,
                                courseSchedule.id,courseClassroom.room_id,is_view)

        setattr(courseSchedule,'is_view',is_view)
        session.add(courseSchedule)
        session.flush()

    return jsonify({'id':courseSchedule.id })


@teacher.route('/subject', methods=['POST'])
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
        description: '教学类型'
        type: 'string'
      teacher_id:
        description: '教师id，不传默认自己'
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
              description: 'teacher_history_id'
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
            grade:
              description: '年级'
              type: 'string'
            type:
              description: '类型'
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
          select th.id,th.`subject_id`,sc.id as subject_category_id,cu.id as curriculum_id,th.subject_name,th.grade,th.type
          from teacher_history th  left join subject su on th.`subject_id` = su.id and su.state <> 99 and su.`delete_flag` = 'IN_FORCE'
          left join subject_category sc on su.`subject_category_id` = sc.id and sc.state <> 99 and sc.`delete_flag` = 'IN_FORCE'
          left join curriculum cu on sc.`curriculum_id` = cu.id and cu.state <> 99 and cu.`delete_flag` = 'IN_FORCE'
          where th.`delete_flag` = 'IN_FORCE'
            ''']

    if 'type' in params.keys():
        sql.append(' and th.type =:type ')
    if 'teacher_id' in params.keys():
        sql.append(' and th.teacher_id =:teacher_id ')
    else:
        sql.append("and th.teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])
    return ['id', 'subject_id', 'subject_category_id','curriculum_id','subject_name', 'grade','type'], ''.join(sql)


@teacher.route('/get_enter_room_url', methods=['POST'])
def get_enter_room_url():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_schedule_id:
        description: '课节id'
        type: 'string'
    res:
      room_id:
        description: '房间号'
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
                                      ClassroomRoleEnum.TEACHER.name,ClassroomDeviceEnum.PC.name)

    return jsonify({'url':url })



@teacher.route('/students', methods=['POST'])
def students():
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
      course_id:
        description: '课程id'
        type: 'string'
      teacher_id:
        description: '教师id，不传默认自己'
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
            student_name:
              description: '学生名称'
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
          select 
                s.id,s.username as student_name
            from  course_schedule cs,study_schedule ss , student s ,course c
            where  cs.id = ss.course_schedule_id and ss.student_id = s.id and cs.course_id = c.id
            and cs.delete_flag = 'IN_FORCE' and ss.`delete_flag` = 'IN_FORCE' 
            ''']

    if 'course_id' in params.keys():
        sql.append(' and c.id =:course_id ')
    if 'teacher_id' in params.keys():
        sql.append(' and c.primary_teacher_id =:teacher_id ')

    sql.append("group by s.id ")

    return ['id', 'student_name'], ''.join(sql)


@teacher.route('/apply_students', methods=['POST'])
def apply_students():
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
              description: 'course_appointment_id操作使用'
              type: 'integer'
            start:
              description: '开始时间'
              type: 'string'
            end:
              description: '结束时间'
              type: 'string'
            student_name:
              description: '学生名称'
              type: 'string'
            apply_state:
              description: '申请状态，0：可以同意，>1:置灰'
              type: 'string'


    """
    j = request.json
    return jsonify(do_query(j, apply_students_sql))


def apply_students_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    current_app.logger.debug(params)
    sql = ['''
          select ca.id,sa.open_time_start as start,sa.open_time_end as end ,s.username as student_name,
          (select count(*) from study_appointment sa1,course_appointment ca1 where sa1.id = ca1.study_appointment_id and sa1.`student_id` = sa.id and ca1.appointment_state = 'ACCEPT') apply_state
           from study_appointment sa,course_appointment ca,student s
          where 
          sa.id = ca.study_appointment_id and sa.student_id = s.id
          and s.`delete_flag` = 'IN_FORCE'  and sa.`delete_flag` = 'IN_FORCE' and ca.`delete_flag` = 'IN_FORCE' 
            ''']

    sql.append("and ca.teacher_id =" + getattr(g, current_app.config['CUR_USER'])['id'])


    return ['id', 'start','end','student_name','apply_state'], ''.join(sql)


@teacher.route('/accept_students', methods=['POST'])
def accept_students():
    """
    swagger-doc: 'schedule'
    required: []
    req:
      course_appointment_id:
        description: '试听申请id'
        type: 'string'
    res:
      id:
        description: 'id'
        type: ''
    """
    course_appointment_id = request.json['course_appointment_id']

    with session_scope(db) as session:

        courseAppointment = session.query(CourseAppointment).filter_by(id=course_appointment_id).one_or_none()

        if courseAppointment is None :
            return jsonify({
                "error": "not found CourseAppointment: {0}".format(
                    course_appointment_id)
            }), 500

        studyAppointment = session.query(StudyAppointment).filter_by(id=courseAppointment.study_appointment_id).one_or_none()

        if studyAppointment is None :
            return jsonify({
                "error": "not found StudyAppointment: {0}".format(
                    course_appointment_id)
            }), 500


        acceptStudyAppointments = session.query(StudyAppointment,CourseAppointment).filter(StudyAppointment.id==CourseAppointment.study_appointment_id and CourseAppointment.appointment_state=='ACCEPT' and StudyAppointment.student_id ==studyAppointment.student_id).all()


        if acceptStudyAppointments is not None or len(acceptStudyAppointments)>0:
            return jsonify({
                "error": "student:{0} have accept ".format(
                    studyAppointment.student_id)
            }), 500

        course =Course( course_type= 1,
                        class_type= 1,
                        classes_number = 1,
                        course_desc = '试听课',
                        state = 98,
                        price= 0,
                        primary_teacher_id = courseAppointment.teacher_id,
                        subject_id = 1,
                        course_name = "Auditions",
                        course_name_zh = '试听课',
                        delete_flag = 'IN_FORCE',
                        updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                        )

        session.add(course)
        session.flush()

        order = Order(
                order_type = 2,
                order_desc = '试听订单',
                amount = 0,
                discount = 0,
                promotion=course.id,
                student_id = studyAppointment.student_id,
                course_id = course.id,
                payment_state = 2,
                channel_id = 1,
                state = 98,
                delete_flag = 'IN_FORCE',
                updated_by=getattr(g, current_app.config['CUR_USER'])['username']
            )

        session.add(order)
        session.flush()

        paylog = PayLog( direction = 1,
                        state = 98,
                        amount = 0,
                        payment_fee = 0,
                        result = 0,
                        order_id= order.id,
                        delete_flag = 'IN_FORCE',
                        state_reason = '试听订单',
                        payment_method = 1,
                        updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                        )
        session.add(paylog)
        session.flush()


        courseschedule = CourseSchedule(
            start = studyAppointment.open_time_start,
            end = studyAppointment.open_time_end,
            name = '试听课',
            state = 98,
            override_course_type=1,
            course_id = course.id,
            schedule_type = 'AUDITIONS',
            delete_flag = 'IN_FORCE',
            updated_by=getattr(g, current_app.config['CUR_USER'])['username']
        )
        session.add(courseschedule)
        session.flush()

        class_type =ClassroomTypeEnum.ONE_VS_ONE.name

        live_service.create_room(getattr(g, current_app.config['CUR_USER'])['username'], courseschedule.id,'试听课', getTimeDiff(studyAppointment.open_time_start,studyAppointment.open_time_end),class_type,studyAppointment.open_time_start,0,'en')

        sudyschedule = StudySchedule(
                actual_start = studyAppointment.open_time_start,
                actual_end = studyAppointment.open_time_end,
                name = '试听课',
                study_state = 1,
                order_id = order.id,
                course_schedule_id = courseschedule.id,
                student_id = studyAppointment.student_id,
                schedule_type = 'AUDITIONS',
                delete_flag = 'IN_FORCE',
                updated_by=getattr(g, current_app.config['CUR_USER'])['username']
        )

        session.add(sudyschedule)
        session.flush()


        return jsonify({'id':courseAppointment.id })



def getTimeDiff(timeStra,timeStrb):
    if timeStra>=timeStrb:
        return 0

    current_app.logger.debug('timeStrb-------->'+timeStrb)

    if "." in timeStra:
        timeStra = timeStra.split('.')[0]
        timeStrb = timeStrb.split('.')[0]

    ta = time.strptime(timeStra, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(timeStrb, "%Y-%m-%d %H:%M:%S")
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)

    secondsDiff=(dataTimeb-dataTimea).seconds
    #两者相加得转换成分钟的时间差
    minutesDiff=round(secondsDiff/60)

    current_app.logger.debug('minutesDiff-------->'+str(minutesDiff))
    return minutesDiff