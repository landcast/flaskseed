#!/usr/bin/env python
from flask import g, jsonify, Blueprint, request, current_app
from src.blueprints import transactional, db_session
from sqlalchemy.sql import *
from src.models import db, Account


test = Blueprint('test', __name__)


@test.route('/add_account_single_session', methods=['POST'])
@transactional(db)
def add_account_single_session():
    j = request.json
    a = Account(state=j['state'], account_name=j['account_name'],
                        account_no=j['account_no'])
    db_session.add(a)
    db_session.flush()
    current_app.logger.debug('id=' + str(a.id))
    return jsonify({'id': str(a.id), 'db_session_id': str(id(db_session))})


@test.route('/add_account_nested_session', methods=['POST'])
@transactional(db)
def add_account_nested_session():
    j = request.json
    a = Account(state=j['state'], account_name=j['account_name'],
                        account_no=j['account_no'])
    db_session.add(a)
    db_session.flush()
    current_app.logger.debug('id=' + str(a.id))
    nested_id = nested_session(a)
    return jsonify({'id': str(a.id), 'db_session_id': str(id(db_session)),
                    'nested_db_session_id': str(nested_id)})


@transactional(db)
def nested_session(account):
    account.state = 2
    db_session.merge(account)
    return id(db_session)