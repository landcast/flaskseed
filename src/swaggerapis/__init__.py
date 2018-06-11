import json
import yaml
from flask import jsonify, Blueprint, redirect
from flask_restless import APIManager
from flask_restless.helpers import *


sqlalchemy_swagger_type = {
    'INTEGER': ('integer', 'int32'),
    'SMALLINT': ('integer', 'int32'),
    'NUMERIC': ('number', 'double'),
    'DECIMAL': ('number', 'double'),
    'VARCHAR': ('string', ''),
    'TEXT': ('string', ''),
    'DATE': ('string', 'date'),
    'BOOLEAN': ('boolean', ''),
    'BLOB': ('string', 'binary'),
    'BYTE': ('string', 'byte'),
    'BINARY': ('string', 'binary'),
    'VARBINARY': ('string', 'binary'),
    'FLOAT': ('number', 'float'),
    'REAL': ('number', 'float'),
    'DATETIME': ('string', 'date-time'),
    'BIGINT': ('integer', 'int64'),
    'ENUM': ('string', ''),
    'INTERVAL': ('string', 'date-time'),
}


class SwagAPIManager(object):
    swagger = {
        'openapi': '3.0.0',
        'info': {
            'description': 'Api definition: Model field has * is required, but '
                           'created_at & updated_at will be set current '
                           'timestamp automatically. The id field should '
                           'be ignored in POST also. The del_flag and state '
                           'are enum and has server default value, can also be '
                           'treated like unrequired. Any field in the form '
                           'like Xxxxx_id is foreign key, which refer to table '
                           'Xxxxx.',
            'version': 'v1'
        },
        'servers': [{'url': 'http://localhost:5000/'}],
        'tags': [],
        'paths': {
            '/upload': {
                'post': {
                    'requestBody': {
                        'content': {
                            'multipart/form-data': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'file': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                                'format': 'binary'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'items': {
                                            'upload_file': {
                                                'type': 'string'
                                            },
                                            'download_file': {
                                                'type': 'string'
                                            }
                                        },
                                        'type': 'array'
                                    }
                                }
                            }
                        }
                    },
                    "tags": [
                        "upload_file"
                    ]
                }
            }
        },
        # global security setting enabled for all endpoints
        # 'security': {
        #     'bearerAuth': []
        # },
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                }
            },
            'schemas': {}
        }
    }

    def setup_swagger_blueprint(self, method, url, model_name, description):
        self.swagger['paths'][url] = {}
        self.swagger['paths'][url][method.lower()] = {
            'description': description,
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': '#/components/schemas/' +
                                    model_name + '_req'
                        }
                    }
                }
            },
            'responses': {
                '200': {
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref':
                                    '#/components/schemas/' +
                                    model_name + '_res'
                            }
                        }
                    },
                    'description': 'Success',
                }
            },
            'tags': [url.split('/')[1]]
        }

    def __init__(self, app=None, **kwargs):
        self.app = None
        self.manager = None
        # iterate all urls, if its docstring contains swagger spec,
        # add it to /swagger
        for url_mapping in app.url_map.iter_rules():
            doc_string = app.view_functions[url_mapping.endpoint].__doc__
            if doc_string:
                app.logger.debug('-----------------------')
                app.logger.debug(url_mapping)
                app.logger.debug(url_mapping.methods)
                app.logger.debug(url_mapping.endpoint)
                app.logger.debug(app.view_functions[url_mapping.endpoint])
                index = doc_string.find('swagger-doc:')
                if index == -1:
                    continue
                swagger_doc = doc_string.replace('swagger-doc:', 'description:')
                swagger_dict = yaml.load(swagger_doc)
                url = str(url_mapping)
                model_name = url.replace('/', '_')
                self.swagger['components']['schemas'][
                    model_name + "_req"] = {
                    'required': swagger_dict['required'],
                    'properties': swagger_dict['req']
                }
                self.swagger['components']['schemas'][
                    model_name + "_res"] = {
                    'properties': swagger_dict['res']
                }
                if 'POST' in url_mapping.methods:
                    self.setup_swagger_blueprint('POST', url, model_name,
                                                 swagger_dict['description'])
                if 'GET' in url_mapping.methods:
                    self.setup_swagger_blueprint('GET', url, model_name,
                                                 swagger_dict['description'])
                if 'PUT' in url_mapping.methods:
                    pass

        if app is not None:
            self.init_app(app, **kwargs)

    def to_json(self, **kwargs):
        return json.dumps(self.swagger, **kwargs)

    def to_yaml(self, **kwargs):
        return yaml.dump(self.swagger, **kwargs)

    def __str__(self):
        return self.to_json(indent=4)

    @property
    def version(self):
        if 'version' in self.swagger['info']:
            return self.swagger['info']['version']
        return None

    @version.setter
    def version(self, value):
        self.swagger['info']['version'] = value

    @property
    def title(self):
        if 'title' in self.swagger['info']:
            return self.swagger['info']['title']
        return None

    @title.setter
    def title(self, value):
        self.swagger['info']['title'] = value

    @property
    def description(self):
        if 'description' in self.swagger['info']:
            return self.swagger['info']['description']
        return None

    @description.setter
    def description(self, value):
        self.swagger['info']['description'] = value

    def add_path(self, model, **kwargs):
        name = model.__tablename__
        schema = model.__name__
        path = kwargs.get('url_prefix', "") + '/' + name
        id_path = "{0}/{{{1}Id}}".format(path, schema.lower())
        self.swagger['paths'][path] = {}
        tag = {
            'name': schema,
            'description': 'Table restful endpoint of ' + name
        }
        self.swagger['tags'].append(tag)
        for method in [m.lower() for m in kwargs.get('methods', ['GET'])]:
            if method == 'get':
                self.swagger['paths'][path][method] = {
                    'tags': [schema],
                    'parameters': [{
                        'name': 'q',
                        'in': 'query',
                        'description': 'searchjson',
                        'required': False,
                        'schema': {'type': 'string'}
                    }],
                    'responses': {
                        200: {
                            'description': 'List ' + schema,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'title': name,
                                        'type': 'array',
                                        'items': {
                                            '$ref': '#/components/schemas/' +
                                                    name
                                        }
                                    }
                                }
                            }
                        }

                    }
                }

                if model.__doc__:
                    self.swagger['paths'][path]['description'] = model.__doc__
                if id_path not in self.swagger['paths']:
                    self.swagger['paths'][id_path] = {}

                self.swagger['paths'][id_path][method] = {
                    'tags': [schema],
                    'parameters': [{
                        'name': schema.lower() + 'Id',
                        'in': 'path',
                        'description': 'ID of ' + schema,
                        'required': False,
                        'schema': {
                            'type': 'integer',
                            'format': 'int64'
                        }
                    }],
                    'responses': {
                        200: {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'title': name,
                                        'type': 'array',
                                        'items': {
                                            '$ref': '#/components/schemas/' +
                                                    name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if model.__doc__:
                    self.swagger['paths'][id_path][
                        'description'] = model.__doc__
            elif method == 'delete':
                if id_path not in self.swagger['paths']:
                    self.swagger['paths'][id_path] = {}
                self.swagger['paths'][
                    "{0}/{{{1}Id}}".format(path, schema.lower())][method] = {
                    'tags': [schema],
                    'parameters': [{
                        'name': schema.lower() + 'Id',
                        'in': 'path',
                        'description': 'ID of ' + schema,
                        'required': True,
                        'schema': {
                            'type': 'integer',
                            'format': 'int64'
                        }
                    }],
                    'responses': {
                        200: {
                            'description': 'Success'
                        }
                    }
                }
                if model.__doc__:
                    self.swagger['paths'][id_path][
                        'description'] = model.__doc__
            elif method == 'post':
                self.swagger['paths'][path][method] = {
                    'tags': [schema],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/' + name
                                }
                            }
                        }
                    },
                    'responses': {
                        200: {
                            'description': 'Success'
                        }

                    }
                }
                if model.__doc__:
                    self.swagger['paths'][path]['description'] = model.__doc__
            elif method == 'put' or method == 'patch':
                if model.__doc__:
                    self.swagger['paths'][path]['description'] = model.__doc__
                if id_path not in self.swagger['paths']:
                    self.swagger['paths'][id_path] = {}

                self.swagger['paths'][id_path][method] = {
                    'tags': [schema],
                    'parameters': [{
                        'name': schema.lower() + 'Id',
                        'in': 'path',
                        'description': 'ID of ' + schema,
                        'required': False,
                        'schema': {
                            'type': 'integer',
                            'format': 'int64'
                        }
                    }],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/' + name
                                }
                            }
                        }
                    },
                    'responses': {
                        200: {
                            'description': 'Success'
                        }

                    }
                }
            else:
                pass

    def add_defn(self, model, **kwargs):
        name = model.__tablename__
        self.swagger['components']['schemas'][name] = {
            'properties': {}
        }
        columns = [c for c in get_columns(model).keys()]
        required = []
        for column_name, column in get_columns(model).items():
            if column_name in kwargs.get('exclude_columns', []):
                continue
            try:
                column_type = str(column.type)
                if '(' in column_type:
                    column_type = column_type.split('(')[0]
                column_defn = sqlalchemy_swagger_type[column_type]
                column_val = {'type': column_defn[0]}
                if column_defn[1]:
                    column_val['format'] = column_defn[1]
                t = column.type
                if hasattr(t, 'native_enum') and t.native_enum:
                    column_val['enum'] = t.enums
                if not column.nullable:
                    required.append(column_name)
                if hasattr(column, 'comment'):
                    column_val['description'] = getattr(column, 'comment')
                self.swagger['components']['schemas'][name]['properties'][
                    column_name] = column_val
            except AttributeError:
                schema = get_related_model(model, column_name)
                associates = schema.__tablename__
                column_defn = {
                    'type': 'array',
                    'items': {
                        '$ref': '#/components/schemas/' + associates
                    }
                }
                if associates + '_id' not in columns:
                    self.swagger['components']['schemas'][name]['properties'][
                        column_name] = column_defn
            self.swagger['components']['schemas'][name]['required'] = required

    def init_app(self, app, **kwargs):
        self.app = app
        self.manager = APIManager(self.app, **kwargs)

        if app and app.debug:
            host = app.config['HOST']
            if host == '0.0.0.0':
                host = '127.0.0.1'
            self.swagger['servers'][0]['url'] = 'http://{}:{}/'.format(
                host, app.config['PORT'])
            if app.config['ESHOST']:
                self.swagger['servers'][0]['url'] = 'http://{}:{}/'.format(
                    app.config['ESHOST'], app.config['PORT'])
                # self.swagger['servers'].append({
                #     'url': 'http://127.0.0.1:5000/'
                # })
            swaggerbp = Blueprint('swagger', __name__,
                                  static_folder='swagger_ui')

            @swaggerbp.route('/swagger')
            def swagger_ui():
                return redirect('/swagger_ui/index.html')

            @swaggerbp.route('/swagger.json')
            def swagger_json():
                # I can only get this from a request context
                return jsonify(self.swagger)

            app.register_blueprint(swaggerbp)

    def create_api(self, model, **kwargs):
        self.manager.create_api(model, **kwargs)
        self.add_defn(model, **kwargs)
        self.add_path(model, **kwargs)
