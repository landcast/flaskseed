from datetime import datetime
import logging
import os
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from flask import Flask, current_app, abort, request, g, jsonify
from flask.json import JSONEncoder
from flask_debugtoolbar import DebugToolbarExtension
import json
import jwt
from src.swaggerapis import SwagAPIManager
from fnmatch import fnmatchcase
import inspect

from src.blueprints.auth import auth, BEARER_TOKEN
from src.blueprints.live import live
from src.blueprints.upload import upload
from src.blueprints.order import order
from src.resources.api import api, admin
from src.models import *
from src.services import mail, redis_store

from src.dbmigrate import migrate
from sqlalchemy.sql.expression import *
from sqlalchemy.orm.properties import ColumnProperty
import urllib
import hashlib


def guess_language_from_request(request):
    langheader = request.headers.get('lang', default=[]) or \
                 request.headers.get('Accept-Language', default=[])
    if not langheader:
        if 'zh' in langheader:
            return 'zh'
        else:
            return 'en'
    else:
        return 'en'


def auth_check_needed(request):
    """
    check the request need to be processed with authtication passed
    before
    :param request:
    :return:
    """
    if str(request.method).upper() in ['OPTIONS', 'HEAD']:
        return False
    path = request.path
    if current_app.debug:
        visitor_allow = ['/', '/*.html', '/*.js', '/*.css', '/*.ico', '/*.jpg',
                         '/auth/*', '/upload', '/download/*', '/admin/*',
                         '/order/*', '/api/*', '/swagger.json',
                         '/static/*', '/swagger_ui/*', '/swagger']
    else:
        visitor_allow = ['/', '/*.html', '/*.js', '/*.css', '/*.ico', '/*.jpg',
                         '/auth/*', '/upload', '/download/*', '/static/*']
    for allow in visitor_allow:
        if fnmatchcase(path, allow):
            return False
    return True


def jwt_check(request):
    jwt_header = request.headers.get(current_app.config['JWT_HEADER'])
    # current_app.logger.debug(jwt_header)
    if jwt_header:
        jwt_token = jwt_header
        if jwt_header.startswith(BEARER_TOKEN):
            jwt_token = jwt_header[len(BEARER_TOKEN):]
        payload = jwt.decode(jwt_token, current_app.config['JWT_SECRET'],
                             algorithm=current_app.config['JWT_ALG'],
                             verify=True)
        current_app.logger.debug(payload)
        return payload
    else:
        return None


def user_load(username):
    setattr(g, current_app.config['CUR_ID'], username)
    if redis_store.exists(username):
        current_app.logger.debug(username + ' already in redis cache')
        setattr(g, current_app.config['CUR_USER'],
                json.loads(redis_store.get('UP:' + username).decode('utf8')))
        return True
    else:
        with session_scope(db) as session:
            for key in user_source:
                table_check = user_source[key]
                rs = session.query(table_check).filter(
                        and_(table_check.username == username,
                             table_check.state != 99)).all()
                if len(rs) > 0:
                    current_app.logger.debug(
                            username + ' set into redis cache')
                    dict = row_dict(rs[0])
                    dict['user_type'] = key
                    setattr(g, current_app.config['CUR_USER'], dict)
                    redis_store.set('UP:' + username,
                                    json.dumps(dict))
                    return True


def init_logging(app):
    # check log file, if not exist create
    basedir = os.path.dirname(app.config['DEBUG_LOGPATH'])
    log_file_path = app.config['DEBUG_LOGPATH']
    if app.debug:
        log_file_path = log_file_path + '_' + str(os.getpid())
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    open(log_file_path + '.log', 'a').close()
    # pass config log path to handler
    file_handler = RotatingFileHandler(
        log_file_path + '.log', maxBytes=1024 * 1024 * 8)
    # file_handler.suffix = "%Y%m%d.log"
    file_handler.setLevel(logging.DEBUG)
    format = '[%(asctime)s] %(levelname)s %(name)s [%(filename)s:%(' \
             'funcName)s:%(lineno)d]: %(message)s'
    file_handler.setFormatter(Formatter(format))
    app.logger.addHandler(file_handler)
    wsgi_logger = logging.getLogger('werkzeug')
    wsgi_logger.addHandler(file_handler)
    # for h in app.logger.handlers:
    #    print('handler is %s' % str(h))


def acl_control(request, response):
    if hasattr(g, current_app.config['CUR_USER']):
        user = getattr(g, current_app.config['CUR_USER'])
        if user['user_type'] not in ['Student', 'Teacher']:
            return
    else:
        return
    parsed = urllib.parse.urlparse(request.url)
    path_atoms = parsed.path.split('/')
    if path_atoms[0] != 'api':
        return
    o_type = path_atoms[2]
    user_id = getattr(g, current_app.config['CUR_ID'])
    current_app.logger.debug('acl_control: setup redis, check data access')
    if request.method.lower() == 'get':
        result = response.get_data().decode('utf-8')
        res_dict = json.loads(result)
        # check acl for student and teacher, if not obey, return 401
        try:
            if res_dict['objects']:
                for o in res_dict['objects']:
                    if not o['id']:
                        continue
                    redis_key = 'ACL:' + user_id + ':' + o_type + ':' + str(
                            o['id'])
                    acl = redis_store.get(redis_key)
                    if not acl:
                        abort(401, redis_key + ' not in redis acl')
                        break
        except Exception as e:
            raise e
        else:
            pass
    elif request.method.lower() == 'post':
        result = response.get_data().decode('utf-8')
        res_dict = json.loads(result)
        redis_key = 'ACL:' + user_id + ':' + o_type + ':' + str(
                res_dict['id'])
        value = hashlib.md5(str(res_dict).encode('utf-8')).hexdigest()
        redis_store.set(redis_key, value)
    elif request.method.lower() == 'put':
        # check for object in request path var belong to user in jwt auth header
        redis_key = 'ACL:' + user_id + ':' + o_type + ':' + path_atoms[3]
        acl = redis_store.get(redis_key)
        if not acl:
            abort(401, redis_key + ' not in redis acl')
    else:
        pass


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                str_datetime = obj.isoformat()
                if len(str_datetime) == 19:
                    # 2019-09-01T19:01:01
                    return obj.isoformat() + '.000Z'
                elif len(str_datetime) == 23:
                    return obj.isoformat() + 'Z'
                elif len(str_datetime) == 26:
                    return obj.isoformat()[:-3] + 'Z'
                else:
                    raise Exception("invalid datetime format " + str_datetime)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app(config):
    app = Flask(__name__)
    # app loading config
    app.config.from_object(config)
    try:
        app.config.from_envvar('EXTERNALCFG')
    except Exception:
        app.logger.warning('EXTERNALCFG not set, config overrding ignored!')
    else:
        app.logger.info('load config overriding from env-var EXTERNALCFG')
    # middle-ware setting app
    init_logging(app)
    api.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    redis_store.init_app(app)

    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
    # create needed folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # register blueprints
    app.register_blueprint(upload)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(live, url_prefix='/live')
    app.register_blueprint(order, url_prefix='/order')
    # register restful endpoints
    app.register_blueprint(admin, url_prefix='/admin')

    manager = SwagAPIManager(app, flask_sqlalchemy_db=db)
    app.manager = manager
    app.json_encoder = CustomJSONEncoder

    @app.before_request
    def request_preprocess():
        # user language process
        lang = request.headers.get('lang', default=None) or \
               request.cookies.get('user_lang', default=None)
        if lang is None:
            language = guess_language_from_request(request)
            setattr(g, 'lang', language)
            current_app.logger.debug('set lang with ' + language)
        # jwt authentication check
        acl_control(request, None)
        if auth_check_needed(request):
            payload = jwt_check(request)
            if payload:
                # user object loading and redis cache setting
                username = payload.get(app.config['JWT_SUBJECT_KEY'])
                if username:
                    current_app.logger.info('auth passed, loading ' + username)
                    user_load(username)
                else:
                    abort(401)
            else:
                # can't find user from jwt_token, return 401
                current_app.logger.warn('auth failed!')
                abort(401)
        else:
            payload = jwt_check(request)
            if payload:
                # user object loading and redis cache setting
                username = payload.get(app.config['JWT_SUBJECT_KEY'])
                if username:
                    current_app.logger.info('auth passed, loading ' + username)
                    if not user_load(username):
                        abort(401, 'failed to load user from cache or db')
            else:
                setattr(g, current_app.config['CUR_ID'],
                        'visitor_' + str(request.remote_addr))
                current_app.logger.debug(
                        'visitor comming')

    @app.after_request
    def request_postprocess(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
        response.headers[
            'Access-Control-Allow-Headers'] = 'x-requested-with, ' \
                                              'Content-type, Authorization, ' \
                                              'lang'
        response.headers['Cache-Control'] = 'no-cache'
        language = g.get('lang', None)
        if language:
            response.headers['Content-Langauge'] = language
            response.set_cookie('user_lang', language)
        if response.is_json and current_app.debug:
            current_app.logger.debug(
                    "\n" + request.method + ': ' + request.url + "\nreq: "
                                                                 "------\n" +
                    request.get_data().decode('utf-8') + "\nres: ------\n" +
                    response.get_data().decode('utf-8'))
            acl_control(request, response)
        return response

    @app.teardown_request
    def request_teardown(exc=None):
        if exc:
            app.log_exception(repr(exc))

    @app.before_first_request
    def setup_api():
        for k, v in globals().items():
            if not (inspect.isclass(v) and issubclass(v, EntityMixin) \
                    and hasattr(v, '__tablename__')):
                continue
            # create endpoint for CRUD and with cascading support for GET
            current_app.manager.create_api(v, url_prefix='/api/v1',
                                           methods=['GET', 'DELETE', 'PUT',
                                                    'POST'],
                                           allow_patch_many=True,
                                           primary_key='id')
            # create bare endpoint for GET without cascading query to improve
            # performance by exclude relation columns
            include_columns = []
            for x in dir(v):
                if (not x.startswith('_')) and isinstance(
                        getattr(getattr(v, x), 'property', None),
                        ColumnProperty):
                    include_columns.append(x)
            current_app.manager.create_api(v, url_prefix='/api/v1/_bare',
                                           methods=['GET'],
                                           include_columns=include_columns,
                                           primary_key='id')

    return app
