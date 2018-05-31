from ustutor.models.common_models import db, EntityMixin
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class Order(EntityMixin, db.Model):
    order_type = Column(Integer, nullable=False)
    order_desc = Column(String(255), nullable=False)
    state = Column(Integer, nullable=False)
    cancel_checkby = Column(String(120), nullable=True,
                            comment="when state change to cancel, this field "
                                    "save the one who approved cancel")
    payment_state = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    promotion = Column(String(255), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'),
                        nullable=False)
    student_orders = db.relationship('Student', backref='student_orders',
                                     lazy=True)
    course_id = Column(Integer, ForeignKey('course.id'),
                       nullable=False)
    course = db.relationship('Course', backref='course_orders', lazy=True)
    channel_id = Column(Integer, ForeignKey('channel.id'),
                        nullable=False)
    channel_orders = db.relationship('Channel', backref='channel_orders',
                                     lazy=True)


class PayLog(EntityMixin, db.Model):
    direction = Column(Integer, nullable=False,
                       comment='receive or return back')
    state = Column(Integer, nullable=False)
    state_reason = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    payment_method = Column(Integer, nullable=False)
    payment_fee = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'),
                      nullable=False)
    order_paylogs = db.relationship('Order', backref='order_paylogs', lazy=True)
    account_id = Column(Integer, ForeignKey('account.id'),
                        nullable=True)
    account_paylogs = db.relationship('Account', backref='account_paylogs',
                                      lazy=True)


class Account(EntityMixin, db.Model):
    state = Column(Integer, nullable=False)
    account_name = Column(String(50), nullable=False)
    account_no = Column(String(50), nullable=False)
    owner_role = Column(Integer, nullable=True)
    owner_id = Column(Integer, nullable=True)
