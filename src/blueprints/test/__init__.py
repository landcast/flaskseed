#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, current_app
from src.blueprints import transactional, db_session
from sqlalchemy.sql import *
from src.models import db, Account


test = Blueprint('test', __name__)


@test.route('/add_account', methods=['POST'])
@transactional(db)
def add_account():
    j = request.json
    # TODO like flask g or current_app, add global proxy support
    db_session.add(Account(state=j['state'], account_name=j['account_name'],
                        account_no=j['account_no']))
    return jsonify({'message': 'succ'})
