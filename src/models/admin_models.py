from src.models.common_models import db, EntityMixin, UserBaseMixin
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from enum import IntFlag


class Enrollment(EntityMixin, db.Model):
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    channel_id = Column(Integer, ForeignKey('channel.id'),
                        nullable=True)
    channel_enrollments = db.relationship('Channel',
                                          backref='channel_enrollments',
                                          lazy=True)


class Channel(EntityMixin, db.Model):
    channel_name = Column(String(255), nullable=False)
    channel_desc = Column(String(255), nullable=True)
    contact_tel = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_address = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)
    domain_address = Column(String(255), nullable=True)
    service_helper = Column(Integer, ForeignKey('sys_user.id'),
                            nullable=True)
    channels = db.relationship('SysUser',
                               backref='serve_channels',
                               lazy=True)


class SysUserState(IntFlag):
    """
    TRAINING: 实习
    WORKING: 正式工作
    """
    TRAINING = 1
    WORKING = 2


class SysUser(UserBaseMixin, db.Model):
    menus = Column(String(2000), nullable=True)
    state = Column(Enum(SysUserState), nullable=False,
                   server_default=SysUserState.WORKING.name)
    user_type = Column(Integer, nullable=True)
    level = Column(String(50), nullable=True)


class Notification(EntityMixin, db.Model):
    notice = Column(String(255), nullable=True)
    state = Column(Integer, nullable=True)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)


class EventLog(EntityMixin, db.Model):
    event_type = Column(Integer, nullable=True)
    event_content = Column(String(8000), nullable=True)


class Attachment(EntityMixin, db.Model):
    attachment_type = Column(Integer, nullable=True)
    file_name = Column(String(255), nullable=True)
    state = Column(Integer, nullable=True)
    mime_type = Column(String(255), nullable=True)
    url_path = Column(String(255), nullable=True)
    size = Column(Integer, nullable=True)
    meta_info = Column(Integer, nullable=True)
    content_type = Column(String(50), nullable=True)
    refer_id = Column(Integer, nullable=True)


class Region(EntityMixin, db.Model):
    pid = Column(Integer, nullable=True)
    path = Column(String(255), nullable=True)
    level = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    name_en = Column(String(255), nullable=True)
    name_pinyin = Column(String(255), nullable=True)
    code = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)


class SmsLog(EntityMixin, db.Model):
    sms_channel = Column(String(50), nullable=True)
    country_code = Column(String(50), nullable=True)
    mobile = Column(String(20), nullable=True)
    content = Column(String(255), nullable=True)
    state = Column(Integer, nullable=False)
    fee = Column(Integer, nullable=False)
    result_code = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)


class Menu(EntityMixin, db.Model):
    menu_name = Column(String(255), nullable=True)
    menu_name_en = Column(String(255), nullable=True)
    state = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=False)
    menu_type = Column(Integer, nullable=False)
    icon_class = Column(String(255), nullable=True)
    expand = Column(Integer, nullable=False)
    sort_no = Column(Integer, nullable=False)
    is_show = Column(Integer, nullable=False)
    permission = Column(String(255), nullable=True)
    remark = Column(String(255), nullable=True)


class FeedBack(EntityMixin, db.Model):
    username = Column(String(50), nullable=True)
    feed_back = Column(String(2000), nullable=True)
    state = Column(Integer, nullable=True)
    process_by = Column(String(50), nullable=True)
    progress = Column(String(50), nullable=True)


class RoleDefinition(EntityMixin, db.Model):
    role_name = Column(String(50), nullable=True)
    role_desc = Column(String(2000), nullable=True)


class SysUserRole(EntityMixin, db.Model):
    sys_user_id = Column(Integer, ForeignKey('sys_user.id'),
                         nullable=False)
    role_definition_id = Column(Integer, ForeignKey('role_definition.id'),
                                nullable=False)


class RoleAuth(EntityMixin, db.Model):
    role_definition_id = Column(Integer, ForeignKey('role_definition.id'),
                                nullable=False)
    auth_target_type = Column(Integer, nullable=False,
                              comment='Auth target type enum menu_id, url, '
                                      'function_name etc')
    auth_target_value = Column(String(2000), nullable=False,
                               comment='Auth target data, '
                                       'could be menu_id, url etc')
    auth_level = Column(Integer, nullable=False, comment='enum view, edit etc')


class SysControl(EntityMixin, db.Model):
    current_pid = Column(Integer, nullable=False)