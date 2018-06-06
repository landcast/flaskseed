from datetime import datetime, timedelta
from flask import current_app
import json
import requests

from src.models import db, session_scope, CourseClassroom, Courseware, \
    CourseClassParticipant, ClassroomRoleEnum, ClassroomTypeEnum, \
    ClassroomStateEnum, CoursewareCheckResultEnum, ClassroomDeviceEnum


def create_room(username, course_schedule_id, title, length,
                room_type=ClassroomTypeEnum.ONE_VS_ONE,
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
    r = requests.post(
        current_app.config['EP_LOCATION'] + current_app.config[
            'EP_LIVE_PATH'] + '/createRoom',
        data=json.dumps({
            'title': title,
            'startTime': start_time,
            'length': length,
            'menNum': room_type.value - 1,
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
                                               room_type=room_type,
                                               state=ClassroomStateEnum.CREATED,
                                               host_code=j['hostCode'],
                                               room_id=j['roomId'],
                                               room_title=title,
                                               duration_start=duration_start,
                                               duration_end=duration_end)
            session.add(course_classroom)
    return r.json()


def edit_room(username, room_id, title=None, length=None,
              start_time=None, user_type=0,
              lang='en'):
    '''
    Edit living teaching room created before.
    :param username: user account name
    :param room_id: room id returned by provider after doing room creation
    :param course_schedule_id: course schedule id
    :param title: room title displayed
    :param length: lecture room service time duration
    :param start_time: room available time
    :param user_type: preserved for future use
    :param lang: user preferred lang
    :return: room edited by third-party provider
    '''
    with session_scope(db) as session:
        course_classroom = session.query(CourseClassroom).filter(
            CourseClassroom.room_id == room_id).one_or_none()
        if not course_classroom:
            raise RuntimeError('CourseClassroom of room_id passed in not found')
        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_LIVE_PATH'] + '/editRoom',
            data=json.dumps({
                'roomId': room_id,
                'title': title,
                'startTime': start_time,
                'length': length,
                'userName': username,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        j = r.json()['room']
        if r.json()['code'] == 0:
            # succ, insert CourseClassroom record
            if title:
                course_classroom.room_title = title
            if start_time:
                course_classroom.duration_start = start_time
            if length:
                course_classroom.duration_end = course_classroom.duration_start \
                                                + timedelta(minutes=length)
            course_classroom.updated_by = username
            session.merge(course_classroom)
    return r.json()


def delete_room(username, room_id):
    '''
    Delete living teaching room.
    :param username: user account name
    :param room_id: room id returned by provider after doing room creation
    :return: room created by third-party provider
    '''
    current_app.logger.debug(room_id)
    with session_scope(db) as session:
        course_classroom = session.query(CourseClassroom).filter(
            CourseClassroom.room_id == room_id).one_or_none()
        if not course_classroom:
            raise RuntimeError('CourseClassroom of room_id passed in not found')
        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_LIVE_PATH'] + '/deleteRoom',
            data=json.dumps({
                'roomId': room_id,
                'userName': username
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            course_classroom.state = ClassroomStateEnum.DELETED
            session.merge(course_classroom)
    return r.json()


def enter_room(username, room_id, nick_name,
               role_in_classroom=ClassroomRoleEnum.ASSISTANT,
               device_type=ClassroomDeviceEnum.PC):
    '''
    Get url for classroom by provide nick_name, role and device_type
    :param username:
    :param room_id: class room created before
    :param nick_name: name displayed in class room
    :param role_in_classroom: ClassroomRoleEnum
    :param device_type: ClassroomDeviceEnum
    :return: url for class room
    '''
    current_app.logger.debug(room_id)
    with session_scope(db) as session:
        course_classroom = session.query(CourseClassroom).filter(
            CourseClassroom.room_id == room_id).one_or_none()
        if not course_classroom:
            raise RuntimeError('CourseClassroom of room_id passed in not found')
        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_LIVE_PATH'] + '/getRoomEnterUrl',
            data=json.dumps({
                'roomId': room_id,
                'userName': username,
                'nickname': nick_name,
                'userRole': role_in_classroom.value - 1,
                'deviceType': device_type.value - 1
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            if course_classroom.room_url:
                temp = eval(course_classroom.room_url)
                temp.append(r.json()['url'])
                course_classroom.room_url = str(temp)
            else:
                course_classroom.room_url = "['{}']".format(r.json()['url'])
            c_c_p = CourseClassParticipant(
                role_in_course=role_in_classroom,
                access_url=r.json()['url'],
                device_type=device_type,
                course_classroom_id=course_classroom.id,
                role_id=nick_name,
                updated_by=username
            )
            session.add(c_c_p)
            session.merge(course_classroom)
    return r.json()


def upload_doc(username, file_url, file_name, course_id):
    '''
    Upload file as courseware into classroom
    :param username:
    :param file_url: courseware file url
    :param file_name: courseware file display name
    :return: uuid refer to uploaded courseware from provider
    '''
    with session_scope(db) as session:
        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_LIVE_PATH'] + '/uploadFileUrl',
            data=json.dumps({
                'filename': file_name,
                'fileUrl': file_url,
                'username': username
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            cw = Courseware(
                ware_desc=file_name,
                ware_url=file_url,
                ware_uid=r.json()['uuid'],
                checked_result=CoursewareCheckResultEnum.BEFORE_CHECK,
                course_id=course_id
            )
            session.add(cw)
    return r.json()


def attach_doc(username, room_id, ware_uid):
    '''
    Attach previously uploaded course ware to specified class room, for teacher
    and student usage during study in class room
    :param username:
    :param room_id: class room created for lecture
    :param ware_uid: previously uploaded course ware uid returned by provider
    :return: None
    '''
    with session_scope(db) as session:
        cw = session.query(Courseware).filter(
            Courseware.ware_uid == ware_uid).one_or_none()
        if cw:
            r = requests.post(
                current_app.config['EP_LOCATION'] + current_app.config[
                    'EP_LIVE_PATH'] + '/attatchDocument',
                data=json.dumps({
                    'documentId': ware_uid,
                    'roomId': room_id,
                    'username': username
                }), headers={'Content-type': 'application/json'})
            current_app.logger.debug(r.text)
            if r.json()['code'] == 0:
                cw.room_id = room_id
                session.merge(cw)
            else:
                raise RuntimeError('calling attachDocument failed')
        else:
            raise RuntimeError(
                'can not find course ware, according to ware_uid')


def remove_doc():
    pass


def preview_doc():
    pass
