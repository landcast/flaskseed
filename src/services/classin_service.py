from datetime import datetime, timedelta
from flask import current_app
import json
import requests

from src.models import db, session_scope, CourseClassroom, Courseware, \
    CourseClassParticipant, ClassroomRoleEnum, ClassroomTypeEnum, \
    ClassroomStateEnum, CoursewareCheckResultEnum, ClassroomDeviceEnum


def register(telephone, nickname, password, user_type=0,lang='en'):
    """
    """
    r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/registre',
            data=json.dumps({
                'telephone': telephone,
                'nickname': nickname,
                'password': password,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
    current_app.logger.debug(r.text)
    with session_scope(db) as session:
        if r.json()['code'] == 0:
            return r.json()['studentId']
        else:
            raise RuntimeError(r.json()['message'])


def addCourse(courseName, expiryTime,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
                current_app.config['EP_LOCATION'] + current_app.config[
                    'EP_CLASSIN_PATH'] + '/addCourse',
                data=json.dumps({
                    'courseName': courseName,
                    'expiryTime': expiryTime,
                    'lang': lang,
                    'userType': user_type,
                }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['courseId']
        else:
            raise RuntimeError(r.json()['message'])


def addCourseStudent(courseId, identity,studentAccount,studentName,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/addCourseStudent',
            data=json.dumps({
                'courseId': courseId,
                'identity': identity,
                'studentAccount': studentAccount,
                'studentName': studentName,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])

def addTeacher(teacherAccount, teacherName,Filedata,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/addTeacher',
            data=json.dumps({
                'teacherAccount': teacherAccount,
                'teacherName': teacherName,
                'Filedata': Filedata,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['teachId']
        else:
            raise RuntimeError(r.json()['message'])


def addOneCourseClass(courseId, className,beginTime,endTime,teacherAccount,teacherName,seatNum,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/addOneCourseClass',
            data=json.dumps({
                'courseId': courseId,
                'className': className,
                'beginTime': beginTime.replace('T', ' ').replace('Z', ''),
                'endTime': endTime.replace('T', ' ').replace('Z', ''),
                'teacherAccount': teacherAccount,
                'teacherName': teacherName,
                'seatNum': seatNum,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['classId']
        else:
            raise RuntimeError(r.json()['message'])


def changeTeacher(courseId, teacherAccount,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/changeTeacher',
            data=json.dumps({
                'courseId': courseId,
                'teacherAccount': teacherAccount,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])


def editTeacher(st_id, teacherName,Filedata,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/editTeacher',
            data=json.dumps({
                'st_id': st_id,
                'teacherName': teacherName,
                'Filedata': Filedata,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])

def delCourseClass(courseId, classId,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/delCourseClass',
            data=json.dumps({
                'courseId': courseId,
                'classId': classId,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])


def delCourse(courseId,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/delCourse',
            data=json.dumps({
                'courseId': courseId,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])

def delCourseStudent(courseId, identity,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/delCourseStudent',
            data=json.dumps({
                'courseId': courseId,
                'identity': identity,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])


def editCourseClass(courseId, classId,className,beginTime,endTime,teacherAccount,teacherName,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/editCourseClass',
            data=json.dumps({
                'courseId': courseId,
                'classId': classId,
                'className': className,
                'beginTime': beginTime.replace('T', ' ').replace('Z', ''),
                'endTime': endTime.replace('T', ' ').replace('Z', ''),
                'teacherAccount': teacherAccount,
                'teacherName': teacherName,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])


def editCourse(courseName, expiryTime,courseId,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/editCourse',
            data=json.dumps({
                'courseId': courseId,
                'courseName': courseName,
                'expiryTime': expiryTime,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])

def editPasswort(telephone, password,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/editPasswort',
            data=json.dumps({
                'telephone': telephone,
                'password': password,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])


def editUserBasic(telephone, nickname,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/editUserBasic',
            data=json.dumps({
                'telephone': telephone,
                'nickname': nickname,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['code']
        else:
            raise RuntimeError(r.json()['message'])

def getTempLoginKey(telephone,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/getTempLoginKey',
            data=json.dumps({
                'telephone': telephone,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['key']
        else:
            raise RuntimeError(r.json()['message'])

def uploadFile(folderId,Filedata,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/uploadFile',
            data=json.dumps({
                'folderId': folderId,
                'Filedata': Filedata,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['fileId']
        else:
            raise RuntimeError(r.json()['message'])

def delFile(folderId,user_type=0,lang='en'):
    """

    """
    with session_scope(db) as session:

        r = requests.post(
            current_app.config['EP_LOCATION'] + current_app.config[
                'EP_CLASSIN_PATH'] + '/delFile',
            data=json.dumps({
                'fileId': folderId,
                'lang': lang,
                'userType': user_type,
            }), headers={'Content-type': 'application/json'})
        current_app.logger.debug(r.text)
        if r.json()['code'] == 0:
            return r.json()['fileId']
        else:
            raise RuntimeError(r.json()['message'])