from functools import wraps
from flask import session, jsonify, g
from .response_code import RET


def login_require(view_func):
    """判断用户是否已经登录"""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        print(session)
        user_name = session.get('name')
        if not user_name:
            return jsonify(status=RET.SESSIONERR, msg='用户未登录')
        else:
            g.user_name = user_name  # 当用户已经登录,用g变量记录用户的名字,方便被装饰的视图直接使用
            return view_func(*args, **kwargs)

    return wrapper
