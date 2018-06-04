from datetime import datetime
from flask import current_app
import json
import requests

from src.models import db, session_scope, CourseClassroom


def create_room(username, course_schedule_id, title, length, room_type=1,
                start_time=datetime.now().isoformat()[:-3] + 'Z', user_type=0,
                lang='en'):
    '''
    Create living teaching room for teach and students.
    :param username: user account name
    :param course_schedule_id: course schedule id
    :param title: room title displayed
    :param length: lecture room service time duration
    :param room_type: 1: 1V1, 2:1VX, 3:Public-lecture
    :param start_time: room available time
    :param user_type: preserved for future use
    :param lang: user preferred lang
    :return: room created by third-party provider
    '''
    current_app.logger.debug(start_time)
    r = requests.post(
        current_app.config['EP_LOCATION'] + current_app.config[
            'EP_LIVE_PATH'] + '/createRoom',
        data=json.dumps({
            'title': title,
            'startTime': start_time,
            'length': length,
            'menNum': room_type,
            'userName': username,
            'lang': lang,
            'userType': user_type,
        }), headers={'Content-type': 'application/json'})
    current_app.logger.debug(r.text)
    j = r.json()['room']
    if r.json()['code'] == 0:
        # succ, insert CourseClassroom record
        with session_scope(db) as session:
            duration_start = datetime.strptime(j['startTime'],
                                               '%Y-%m-%dT%H:%M:%S.%fZ')
            duration_end = datetime.strptime(j['endTime'],
                                               '%Y-%m-%dT%H:%M:%S.%fZ')
            course_classroom = CourseClassroom(provider=1,
                                               course_schedule_id=course_schedule_id,
                                               video_ready=1,
                                               updated_by=username,
                                               room_type=room_type, state=1,
                                               host_code=j['hostCode'],
                                               room_id=j['roomId'],
                                               room_title=title,
                                               duration_start=duration_start,
                                               duration_end=duration_end)
            session.add(course_classroom)
    return r.json()


def edit_room(username, room_id, title, length, room_type=1,
              start_time=datetime.now().isoformat()[:-3] + 'Z', user_type=0,
              lang='en'):
    '''
    Edit created living teaching room information.
    :param username:
    :param room_id:
    :param title:
    :param length:
    :param room_type:
    :param start_time:
    :param user_type:
    :param lang:
    :return:
    '''
    pass


def delete_room():
    pass


def enter_room():
    pass


def upload_doc():
    pass


def attach_doc():
    pass


def remove_doc():
    pass


def preview_doc():
    pass
