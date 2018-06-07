#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.sql import *
import json
import jwt
import random
import requests

from src.models import db, session_scope, user_source, SmsLog
from src.service import send_email, redis_store
from src.service import live_service

live = Blueprint('live', __name__)


def retrieve_username():
    username = getattr(g, current_app.config['CUR_ID'])
    if not username and current_app.debug:
        username = request.json['username']
    return username


@live.route('/create_room', methods=['POST'])
def create_room():
    """
    swagger-doc: 'Create living teaching room for teach and students.'
    required: ['username', 'course_schedule_id', 'title']
    req:
      username:
        description: 'login user name'
        type: 'string'
      course_schedule_id:
        description: 'course schedule id'
        type: 'integer'
      title:
        description: 'room title displayed'
        type: 'string'
      length:
        description: 'lecture room service time duration in minutes, default=60'
        type: 'integer'
      room_type:
        description: 'ONE_VS_ONE, ONE_VS_MANY, PRIVATE_CLASS, PUBLIC_CLASS,
        default=ONE_VS_ONE'
        type: 'string'
        enum: [ONE_VS_ONE, ONE_VS_MANY, PRIVATE_CLASS, PUBLIC_CLASS]
      start_time:
        description: 'room available time, default=current-timestamp'
        type: 'string'
    res:
      title:
        description: 'room title displayed'
        type: 'string'
      startTime:
        description: 'room available time'
        type: 'string'
      endTime:
        description: 'room closed time'
        type: 'string'
      roomId:
        description: 'room id returned after creation'
        type: 'string'
      hostCode:
        description: 'host code for room participants invitation'
        type: 'string'
      video:
        description: 'room enabled video'
        type: 'boolean'
    """
    j = request.json
    username = retrieve_username()
    r = live_service.create_room(username, j['course_schedule_id'], j['title'],
                                 j['length'], j['room_type'], j['start_time'])
    return jsonify(r)


@live.route('/edit_room', methods=['POST'])
def edit_room():
    """
    swagger-doc: 'Edit living teaching room created before.'
    required: ['username', 'room_id']
    req:
      username:
        description: 'login user name'
        type: 'string'
      course_schedule_id:
        description: 'course schedule id'
        type: 'integer'
      title:
        description: 'room title displayed'
        type: 'string'
      length:
        description: 'lecture room service time duration in minutes, default=60'
        type: 'integer'
      room_id:
        description: 'room id returned after creation'
        type: 'string'
      start_time:
        description: 'room available time, default=current-timestamp'
        type: 'string'
    res:
    """
    j = request.json
    username = retrieve_username()
    live_service.edit_room(username, j['room_id'], j['title'],
                           j['length'], j['start_time'])
    return jsonify({})


@live.route('/delete_room', methods=['POST'])
def delete_room():
    """
    swagger-doc: 'Delete living teaching room.'
    required: ['username', 'room_id']
    req:
      username:
        description: 'login user name'
        type: 'string'
      room_id:
        description: 'room id returned after creation'
        type: 'string'
    res:
    """
    j = request.json
    username = retrieve_username()
    live_service.delete_room(username, j['room_id'])
    return jsonify({})


@live.route('/enter_room', methods=['POST'])
def enter_room():
    """
    swagger-doc: 'Get url for classroom by provide nick_name, role and
    device_type'
    required: ['username', 'room_id', 'nick_name']
    req:
      username:
        description: 'login user name'
        type: 'string'
      room_id:
        description: 'room id returned after creation'
        type: 'string'
      nick_name:
        description: 'login user name displayed in room'
        type: 'string'
      role_in_classroom:
        description: 'AUDIENCE, TEACHER, STUDENT, SIT_IN, ASSISTANT,
        default=ASSISTANT'
        type: 'string'
        enum: [AUDIENCE, TEACHER, STUDENT, SIT_IN, ASSISTANT]
      device_type:
        description: 'PC, PHONE, default=PC'
        type: 'string'
        enum: [PC, PHONE]
    res:
      room_url:
        description: 'url for entering room'
        type: 'string'
    """
    j = request.json
    username = retrieve_username()
    r = live_service.enter_room(username, j['room_id'], j['nick_name'],
                                j['role_in_classroom'], j['device_type'])
    return jsonify({'room_url': r})


@live.route('/upload_doc', methods=['POST'])
def upload_doc():
    """
    swagger-doc: 'Upload file as courseware into classroom'
    required: ['username', 'file_url', 'file_name']
    req:
      username:
        description: 'login user name'
        type: 'string'
      file_url:
        description: 'courseware file url'
        type: 'string'
      file_name:
        description: 'courseware file display name'
        type: 'string'
      course_id:
        description: 'course id'
        type: 'integer'
    res:
      ware_uid:
        description: 'url for entering room'
        type: 'string'
    """
    j = request.json
    username = retrieve_username()
    r = live_service.upload_doc(username, j['file_url'], j['file_name'],
                                j['course_id'])
    return jsonify({'ware_uid': r})


@live.route('/attach_doc', methods=['POST'])
def attach_doc():
    """
    swagger-doc: 'Attach previously uploaded course ware to specified class
    room, for teacher and student usage during study in class room'
    required: ['username', 'room_id', 'ware_uid']
    req:
      username:
        description: 'login user name'
        type: 'string'
      room_id:
        description: 'class room created for lecture'
        type: 'string'
      ware_uid:
        description: 'previously uploaded course ware uid returned by provider'
        type: 'string'
    res:
    """
    j = request.json
    username = retrieve_username()
    live_service.attach_doc(username, j['room_id'], j['ware_uid'])
    return jsonify({})


@live.route('/remove_doc', methods=['POST'])
def remove_doc():
    """
    swagger-doc: 'Remove attached course ware from room'
    required: ['username', 'room_id', 'ware_uid']
    req:
      username:
        description: 'login user name'
        type: 'string'
      room_id:
        description: 'class room created for lecture'
        type: 'string'
      ware_uid:
        description: 'previously uploaded course ware uid returned by provider'
        type: 'string'
    res:
    """
    j = request.json
    username = retrieve_username()
    live_service.remove_doc(username, j['room_id'], j['ware_uid'])
    return jsonify({})


@live.route('/preview_doc', methods=['POST'])
def preview_doc():
    """
    swagger-doc: 'Get course ware preview url'
    required: ['username', 'ware_uid']
    req:
      username:
        description: 'login user name'
        type: 'string'
      ware_uid:
        description: 'previously uploaded course ware uid returned by provider'
        type: 'string'
    res:
      ware_url:
        description: 'preview course ware url'
        type: 'string'
    """
    j = request.json
    username = retrieve_username()
    r = live_service.upload_doc(username, j['ware_uid'])
    return jsonify({'ware_url': r})
