import logging
import os
from logging import FileHandler, Formatter
from flask import Flask, abort
from ustutor.swaggerapis import SwagAPIManager
from fnmatch import fnmatchcase
import inspect
import json

from ustutor.blueprints.auth import *
from ustutor.blueprints.upload import upload
from ustutor.resources.api import api, admin
from ustutor.models import *
from ustutor.service import mail, redis_store

from ustutor.dbmigrate import migrate
from sqlalchemy.sql.expression import *


def setup_api(manager):
    for k, v in globals().items():
        if inspect.isclass(v) and issubclass(v, EntityMixin) \
                and hasattr(v, '__tablename__'):
            # print(getattr(v, '__tablename__'))
            manager.create_api(v, url_prefix='/api/v1',
                               methods=['GET', 'DELETE', 'PUT', 'POST'],
                               allow_patch_many=True,
                               primary_key='id')


def create_app(config):
    app = Flask(__name__)
    # app loading config
    app.config.from_object(config)
    try:
        app.config.from_envvar('USTUTORCONFIG')
    except Exception:
        app.logger.warn('USTUTORCONFIG not set, config overrding ignored!')
    else:
        app.logger.info('load config overriding from env-var USTUTORCONFIG')

    # print('ESHOST=', app.config['ESHOST'])

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
        ''' check the request need to be processed with authtication passed
        before
        '''
        path = request.path
        visitor_allow = ['/', '/*.html', '/*.js', '/*.css', '/*.ico', '/*.jpg',
                         '/auth/*', '/upload', '/download/*', '/admin/*',
                         '/api/*', '/swagger.json',
                         '/static/*', '/swagger_ui/*', '/swagger']
        for allow in visitor_allow:
            if fnmatchcase(path, allow):
                return False
        return True

    def jwt_check(request):
        jwt_header = request.headers.get(app.config['JWT_HEADER'])
        # current_app.logger.debug(jwt_header)
        if jwt_header:
            jwt_token = jwt_header
            if jwt_header.startswith(BEARER_TOKEN):
                jwt_token = jwt_header[len(BEARER_TOKEN):]
            payload = jwt.decode(jwt_token, app.config['JWT_SECRET'],
                                 algorithm=app.config['JWT_ALG'], verify=True)
            current_app.logger.debug(payload)
            return payload
        else:
            return None

    def user_load(username):
        setattr(g, current_app.config['CUR_ID'], username)
        if redis_store.exists(username):
            current_app.logger.debug(username + ' already in redis cache')
        else:
            with session_scope(db) as session:
                for table_check in user_source.values():
                    rs = session.query(table_check).filter(
                        and_(table_check.username == username,
                             table_check.state == 1)).all()
                    if len(rs) > 0:
                        current_app.logger.debug(
                            username + ' set into redis cache')
                        redis_store.set('UP:' + username,
                                        json.dumps(row_dict(rs[0])))
                        break

    def init_logging(app):
        file_handler = FileHandler("debug.log")
        file_handler.setLevel(logging.DEBUG)
        format = '[%(asctime)s] %(levelname)s %(name)s [%(filename)s:%(' \
                 'funcName)s:%(lineno)d]: %(message)s'
        file_handler.setFormatter(Formatter(format))
        app.logger.addHandler(file_handler)
        wsgi_logger = logging.getLogger('werkzeug')
        wsgi_logger.addHandler(file_handler)
        # for h in app.logger.handlers:
        #    print('handler is %s' % str(h))

    # middle-ware setting app
    init_logging(app)
    api.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    redis_store.init_app(app)

    # create needed folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # register blueprints
    app.register_blueprint(upload)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    manager = SwagAPIManager(app, flask_sqlalchemy_db=db)
    setup_api(manager)

    # manager.create_api(Curriculum, url_prefix='/api/v1',
    #                    methods=['GET', 'DELETE', 'PUT', 'POST'],
    #                    primary_key='id')

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
            setattr(g, current_app.config['CUR_ID'],
                    'visitor_' + str(request.remote_addr))
            current_app.logger.debug('visitor comming ' + request.url)

    @app.after_request
    def request_postprocess(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
        response.headers[
            'Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        response.headers['Cache-Control'] = 'no-cache'
        language = g.get('lang', None)
        if language:
            response.headers['Content-Langauge'] = language
            response.set_cookie('user_lang', language)
        return response

    @app.teardown_request
    def request_teardown(exc=None):
        if exc:
            app.log_exception(repr(exc))

    return app
