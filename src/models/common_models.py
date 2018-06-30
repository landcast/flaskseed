import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Float, Enum
from contextlib import contextmanager
from datetime import datetime

db = SQLAlchemy()


@contextmanager
def session_scope(db):
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except (IOError, ValueError) as err:
        session.rollback()
        raise
    finally:
        pass


def row_dict(row):
    result = {c.name: str(getattr(row, c.name)) for c in
              row.__table__.columns}
    return result


class DeleteEnum(enum.IntEnum):
    """
    Using enum.IntEnum instead of enum.Enum
    because this class instance will be used
    for json serialization, the enum.Enum
    not support json.dumps(obj)
    The start value should be from 1, not 0
    because generated mysql enum using
    1 as start value by default
    """
    IN_FORCE = 1
    DELETED = 2


class EntityMixin(object):
    id = Column(Integer, primary_key=True)
    delete_flag = Column(Enum(DeleteEnum), nullable=False,
                         server_default=DeleteEnum.IN_FORCE.name)
    created_at = Column(DateTime, nullable=False, default=datetime.now,
                        comment='created time')
    updated_at = Column(DateTime, nullable=False, default=datetime.now,
                        onupdate=datetime.now,
                        comment='last updated time')
    updated_by = Column(String(60), nullable=True,
                        comment='last updated operator name')


class UserBaseMixin(EntityMixin):
    username = Column(String(60), nullable=False, unique=True,
                      comment='user provided unique name')
    password = Column(String(255), nullable=False,
                      comment='user provided password with cryption')
    mobile = Column(String(20), nullable=True,
                    comment='mobile/tel no provided by user')
    email = Column(String(60), nullable=True,
                   comment='email address provided by user')
    gender = Column(Integer, nullable=True, comment='gender/sex')
    birth = Column(DateTime, nullable=True, comment='user birth date')
    avatar = Column(String(255), nullable=True, comment='user logo image url')
    lang = Column(String(20), nullable=True, comment='user language setting')
    verify_type = Column(String(20), nullable=True,
                         comment='user info verify type')
    nickname = Column(String(20), nullable=True, comment='user nick name')
    user_tag = Column(String(20), nullable=True, comment='user tag')
    last_login_ip = Column(String(20), nullable=True)
    last_login_time = Column(DateTime, nullable=True)
    last_login_device = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True, comment='first name')
    middle_name = Column(String(50), nullable=True, comment='middel name')
    last_name = Column(String(50), nullable=True, comment='last name')
    govtid_type = Column(Integer, nullable=True,
                         comment='government identity type')
    govtid = Column(String(50), nullable=True, comment='government identity no')
    profession = Column(String(50), nullable=True)
    profile = Column(String(255), nullable=True, comment='self introduction')
    organization = Column(String(255), nullable=True,
                          comment='belonging organization description')
    home_address = Column(String(255), nullable=True)
    office_address = Column(String(255), nullable=True)
    location_lng = Column(Float, nullable=True, comment='longitude value of GPS')
    location_lat = Column(Float, nullable=True, comment='latitude value of GPS')
    social_token = Column(String(255), nullable=True, comment='oauth token')
    im_token = Column(String(255), nullable=True,
                      comment='im saas services token')
    class_token = Column(String(255), nullable=True,
                         comment='class-room services user token')
