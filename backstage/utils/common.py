from functools import wraps
from flask import session, jsonify, g, current_app
from .response_code import RET
from backstage.sql import SqlHelper
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from config import Config


# def login_require(view_func):
#     """判断用户是否已经登录"""
#
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#         user_name = session.get('name')
#         if not user_name:
#             return jsonify(status=RET.SESSIONERR, msg='用户未登录')
#         else:
#             g.user_name = user_name  # 当用户已经登录,用g变量记录用户的名字,方便被装饰的视图直接使用
#             return view_func(*args, **kwargs)

    # return wrapper


def admin_require(view_func):
    """判断用户是否有管理员权限"""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        name = session.get('name')
        result = SqlHelper.fetch_one('select role from user where name=%s', [name])
        if result['role'] != '管理员':
            return jsonify(status=RET.PERMISSIONERR, msg='权限不足')
        else:
            return view_func(*args, **kwargs)

    return wrapper


def generate_token(name):
    expiration = 7200
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration) #expiration是过期时间
    token = s.dumps({'name': name}).decode('ascii')
    return token


def certify_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
        return data
    except SignatureExpired:
        return None  # valid token,but expired
    except BadSignature:
        return None  # invalid token


def login_require(token):
    if token:
        if not certify_token(token):
            return "超时登录"
    else:
        return None