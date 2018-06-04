from datetime import datetime
from flask import current_app
import json
import requests


def create_room(title, length, menNum,
                start_time=datetime.now().isoformat()[:-3] + 'Z'):
    '''
    create living room for teacher and students
    :param title:
    :param length:
    :param menNum:
    :param start_time:
    :return: room created information
    '''
    current_app.logger.debug(start_time)
    r = requests.post(
        current_app.config['EP_LOCATION'] + current_app.config[
            'EP_LIVE_PATH'] + '/createRoom',
        data=json.dumps({
            'title': 'test extport live room',
            'startTime': start_time,
            'length': 60,
            'menNum': 1
        }), headers={'Content-type': 'application/json'})
    current_app.logger.debug(r.text)


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
