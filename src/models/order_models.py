from src.models.common_models import db, EntityMixin
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from enum import IntFlag


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
                       comment='收款还是付款,1:收款，2：付款')
    state = Column(Integer, nullable=False,comment='状态')
    state_reason = Column(String(255), nullable=False,comment='该状态原因')
    amount = Column(Integer, nullable=False,comment='退款金额')
    result = Column(Integer, nullable=False,comment='最终退款金额')
    payment_method = Column(Integer, nullable=False,comment='支付，退款方式')
    payment_fee = Column(Integer, nullable=False,comment='订单支付费用')
    remark = Column(String(1000), nullable=True,comment='备注信息')
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


class OrderStateEnum(IntFlag):
    """
    EFFECTIVE:有效
    INVALID:无效
    """
    EFFECTIVE = 98
    INVALID = 99

class OrderPaymentStateEnum(IntFlag):
    """
    PAY：下订单
    PAID :已经付款
    CANCEL : 取消
    APPLY_REFUND:申请退款
    CHECK_PASSED 审核通过
    CHECK_DENY 审核驳回
    REFUND :退款
    USED :已经使

    """

    PAY = 1
    PAID =2
    CANCEL =3
    APPLY_REFUND = 4
    CHECK_PASSED = 5
    CHECK_DENY = 6
    REFUND =7
    USED=8


class OrderTypeEnum(IntFlag):
    """
    COMMON :普通订单
    GIVE :赠送订单
    COMPENSATE :补偿订单
    FREE :免费订单
    REFUND:退款订单
    AUDITIONS:试听
    """
    COMMON = 1
    GIVE = 2
    COMPENSATE = 3
    FREE = 4
    REFUND = 5
    AUDITIONS = 6


class PaymentMethodEnum(IntFlag):
    """
    UNDER_LINE :线下支付
    """
    UNDER_LINE = 1



