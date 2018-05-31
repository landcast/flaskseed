#!/usr/bin/env python
from flask_restful import Resource


class CurriculumApi(Resource):

    def get(self, id=None):
        return {'code': 0, 'id': id}

    def post(self, id=None):
        return {'code': 0, 'id': id}, 201


class SubjectApi(Resource):

    def get(self, id=None):
        return {'code': 0, 'id': id}

    def post(self, id=None):
        return {'code': 0, 'id': id}, 201


class CourseApi(Resource):

    def get(self, id=None):
        return {'code': 0, 'id': id}

    def post(self, id=None):
        return {'code': 0, 'id': id}, 201


class CourseScheduleApi(Resource):

    def get(self, id=None):
        return {'code': 0, 'id': id}

    def post(self, id=None):
        return {'code': 0, 'id': id}, 201

