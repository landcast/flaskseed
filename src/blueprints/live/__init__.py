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


@live.route('/create-room', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/edit-room', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/delete-room', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/enter-room', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/upload-doc', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/attach-doc', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/remove-doc', methods=['POST'])
def create_room():
    return jsonify({})


@live.route('/preview-doc', methods=['POST'])
def create_room():
    return jsonify({})
