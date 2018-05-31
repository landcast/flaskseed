from flask_restful import Api
from flask import Blueprint

from src.resources.todo_api import TodoSimple
from src.resources.admin_api import CourseApi, CourseScheduleApi, \
    CurriculumApi, \
    SubjectApi

api = Api()
api.add_resource(TodoSimple, '/todos/<string:todo_id>')

admin = Blueprint('admin', 'admin', url_prefix='/admin')
api_admin = Api(admin)
api_admin.add_resource(CurriculumApi, '/curriculum/<int:id>')
api_admin.add_resource(CourseApi, '/course/<int:id>')
api_admin.add_resource(CourseScheduleApi, '/course_schedule/<int:id>')
api_admin.add_resource(SubjectApi, '/subject', '/subject/<int:id>')
