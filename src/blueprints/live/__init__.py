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


live = Blueprint('live', __name__)


@live.route('/create_room', methods=['POST'])
def create_room():
    '''

    :return:
    '''
    return jsonify({})


@live.route('/edit_room', methods=['POST'])
def edit_room():
    return jsonify({})


@live.route('/delete_room', methods=['POST'])
def delete_room():
    return jsonify({})


@live.route('/enter_room', methods=['POST'])
def enter_room():
    return jsonify({})


@live.route('/upload_doc', methods=['POST'])
def upload_doc():
    return jsonify({})


@live.route('/attach_doc', methods=['POST'])
def attach_doc():
    return jsonify({})


@live.route('/remove_doc', methods=['POST'])
def remove_doc():
    return jsonify({})


@live.route('/preview_doc', methods=['POST'])
def preview_doc():
    return jsonify({})
