#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, current_app
from src.services import do_query, datetime_param_sql_format
from sqlalchemy.sql import *
from src.models import db, session_scope, Course,Order,PayLog,Student,Teacher,Subject,CourseSchedule

order = Blueprint('order', __name__)


@order.route('/main_query', methods=['POST'])
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
        description: 'course name 课程名称'
        type: 'string'
      course_id:
        description: 'course id 课程编号'
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
    return jsonify(do_query(
        datetime_param_sql_format(j, ['created_at_start', 'created_at_end']),
        generate_sql))


def generate_sql(params):
    '''
    generate dynamic sql for order query by params
    :param params:
    :return:
    '''
    sql = ['''
    select o.id, c.course_name, c.classes_number, o.order_type, o.state,
        o.updated_by, o.created_at, concat(t.first_name,' ',t.middle_name,' ',t.last_name) as teacher_name, s.name as student_name, o.amount as order_amount
    from `order` o, student s, teacher t, course c, subject su,
    subject_category sc, curriculum cr
    where o.student_id = s.id and o.course_id = c.id and
        c.primary_teacher_id = t.id and c.subject_id = su.id and
        su.curriculum_id = cr.id and su.subject_category_id = sc.id
    ''']
    if 'course_id' in params.keys():
        sql.append(' and c.id = :course_id')
    if 'course_name' in params.keys():
        sql.append(' and c.course_name = :course_name')
    if 'order_type' in params.keys():
        sql.append(' and o.order_type = :order_type')
    if 'order_state' in params.keys():
        sql.append(' and o.state = :order_state')
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
    sql.append(' order by o.id desc')
    current_app.logger.debug(sql)
    return ['id', 'course_name', 'classes_number', 'order_type', 'order_state',
            'updated_by', 'created_at', 'teacher_name', 'student_name',
            'order_amount'], ''.join(sql)


@order.route('/establish', methods=['POST'])
def establish():
    """
    swagger-doc: 'establish'
    required: []
    req:
      order_type:
        description: '订单类型'
        type: 'string'
      have_course:
        description: '存在课包：1，不存在：0'
        type: 'integer'
      course_id:
        description: '课程包id'
        type: 'integer'
      student:
        description: '学生账号或id'
        type: 'string'
      subject_id:
        description: '第三节分类id'
        type: 'integer'
      course_type:
        description: '1:公共，2在线'
        type: 'integer'
      class_type:
        description: '班级，常量'
        type: 'integer'
      project_type:
        description: '班级，常量'
        type: 'integer'
      teacher:
        description: '教师账号或id'
        type: 'string'
      classes_number:
        description: '课程节数'
        type: 'integer'
      basic_amount:
        description: '基本价格'
        type: 'integer'
      amount:
        description: '金额'
        type: 'integer'
      order_desc:
        description: '订单描述'
        type: 'string'
    res:
      id:
        description: 'order id'
        type: 'string'
    """
    order_type = request.json['order_type']
    course_id ='0'
    if 'course_id' in request.json:
        course_id = request.json['course_id']
    student_parm = request.json['student']

    amount = request.json['amount']
    order_desc = request.json['order_desc']

    with session_scope(db) as session:
        if student_parm.isdigit():
            student = session.query(Student).filter_by(
                id=student_parm).one_or_none()
        else:
            student = session.query(Student).filter_by(
                username=student_parm).one_or_none()

        if student is None:
            return jsonify({
                "error": "not found student:{0} ".format(
                    student_parm)
            }), 500

        student_id = getattr(student, 'id')

        if 'have_course' in request.json and request.json['have_course'] == 0:

            teacher_parm = request.json['teacher']
            course_type = request.json['course_type']
            class_type = request.json['class_type']
           # project_type = request.json['project_type']

            classes_number = request.json['classes_number']
            basic_amount = request.json['basic_amount']
            subject_id = request.json['subject_id']

            subject = session.query(Subject).filter_by(id=subject_id).one_or_none()

            if subject is None:
                return jsonify({
                    "error": "not found subject: {0}".format(
                        subject_id)
                }), 500

            if teacher_parm.isdigit():
                teacher = session.query(Teacher).filter_by(id=teacher_parm).one_or_none()
            else:
                teacher = session.query(Teacher).filter_by(username=teacher_parm).one_or_none()

            subject = session.query(Subject).filter_by(id=subject_id).one_or_none()

            if teacher is None:
                return jsonify({
                    "error": "not found teacher: {0}".format(
                        teacher_parm)
                }), 500

            teacher_id = getattr(teacher, 'id')

            course_name = getattr(subject, 'subject_name')

            course_name_zh = getattr(subject, 'subject_name_zh')

            course =Course( course_type= course_type,
                            class_type= class_type,
                            classes_number = classes_number,
                            course_desc = order_desc,
                            state = 98,
                            price= basic_amount,
                            primary_teacher_id = teacher_id,
                            subject_id = subject_id,
                            course_name = course_name,
                            course_name_zh = course_name_zh,
                            delete_flag = 'IN_FORCE',
                            updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                )

            session.add(course)
            session.flush()

            amount = int(classes_number)*int(basic_amount)

            course_id = getattr(course, 'id')



        course = session.query(Course).filter_by(id=course_id).one_or_none()

        orders = session.query(Order).filter_by(course_id = course_id, state=98,delete_flag = 'IN_FORCE').all()


        if len(orders) > course.class_type:
            return jsonify({
                "error": "class_type error"
            }), 500


        sourseSchedules = session.query(CourseSchedule).filter_by(course_id = course_id, state=98,delete_flag = 'IN_FORCE').all()

        if sourseSchedules is not None and len(sourseSchedules) > 0:
            return jsonify({
                "error": "found order {0} have sourse schedules".format(
                    course_id)
            }), 500



        order = Order(
            order_type = order_type,
            order_desc = order_desc,
            amount = amount,
            discount = amount,
            promotion=course_id,
            student_id = student_id,
            course_id = course_id,
            payment_state = 1,
            channel_id = 1,
            state = 98,
            delete_flag = 'IN_FORCE',
            updated_by=getattr(g, current_app.config['CUR_USER'])['username'],
            created_by=getattr(g, current_app.config['CUR_USER'])['id']
        )

        result = session.add(order)
        session.flush()

        order_id = getattr(order, 'id')

        paylog = PayLog( direction = 1,
                        state = 98,
                        amount = amount,
                        payment_fee = amount,
                        result = amount,
                        order_id= order_id,
                        delete_flag = 'IN_FORCE',
                        state_reason = 'establish',
                        payment_method = 1,
                        updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                )
        session.add(paylog)
        session.flush()

    return jsonify({'id':order_id })


@order.route('/refund', methods=['POST'])
def refund():
    """
    swagger-doc: 'refund'
    required: []
    req:
      order_id:
        description: '订单id'
        type: 'string'
      reason:
        description: '原因'
        type: 'string'
      amount:
        description: '金额'
        type: 'integer'
      order_desc:
        description: '描述'
        type: 'string'
    res:
      id:
        description: 'id'
        type: 'string'
    """
    order_id = request.json['order_id']
    reason = request.json['reason']
    amount = request.json['amount']
    order_desc = request.json['order_desc']

    with session_scope(db) as session:

        order = session.query(Order).filter_by(
                id=order_id).one_or_none()

        if order is None:
            return jsonify({
                "error": "not found order_id:{0} ".format(
                    order_id)
            }), 500

        setattr(order,'order_type',4)

        setattr(order,'payment_state',7)

        session.add(order)

        session.flush()

        paylog = PayLog( direction = 2,
                         state = 4,
                         amount = amount,
                         payment_fee = amount,
                         result = amount,
                         order_id= order_id,
                         state_reason = reason,
                         remark= order_desc,
                         delete_flag = 'IN_FORCE',
                         payment_method = 1,
                         updated_by=getattr(g, current_app.config['CUR_USER'])['username']
                         )
        session.add(paylog)

        session.flush()

    return jsonify({'id':order_id })
