#!/usr/bin/env python
from flask import request, g, current_app
from flask_restful import Resource


todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        current_app.logger.debug(g.get(current_app.config['CUR_ID'], '') + ' submitted put todo item')
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201

