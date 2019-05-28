from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(object):
    """模型基类"""
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now)


class User(BaseModel):
    """用户模型"""

    __tablename__ = 'bk_user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    job_number = db.Column(db.String(15), nullable=False)
    real_name = db.Column(db.String(32), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    id_card_number = db.Column(db.String(25), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)




class Order(BaseModel):
    """订单信息表"""

    __tablename__ = 'db_order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    id_card_number = db.Column(db.String(25), nullable=False)
    bank_card_number = db.Column(db.String(32), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    recommand_jod_number = db.Column(db.String(15), nullable=False)
    pre_paid_amount = db.Column(db.Integer, nullable=False)
    paid_status = db.Column(db.Boolean, unique=False, default=0)
    paid_time = db.Column(db.DateTime, nullable=False)


class Info(BaseModel):
    """系统信息设置"""

    __tablename__ = 'bk_info'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    qrcode_url = db.Column(db.String(150), nullable=False)





