from datetime import datetime
from flask import current_app
import json
import requests


def create_room(username, title, length, room_type=1,
                start_time=datetime.now().isoformat()[:-3] + 'Z', user_type=0,
                lang='en'):
    '''
    Create living teaching room for teach and students.
    :param title:
    :param length:
    :param room_type: 1: 1V1, 2:1VX, 3:Public-lecture
    :param username:
    :param start_time:
    :param user_type:
    :param lang:
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
            'username': username,
            'lang': lang,
            'userType': user_type,
        }), headers={'Content-type': 'application/json'})
    current_app.logger.debug(r.text)
    return r.json()


def edit_room():
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
