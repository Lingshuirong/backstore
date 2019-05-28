import base64
import time
import hmac
import re
from flask import request, session, g, current_app, jsonify
from . import api
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.common import login_require


@api.route('/register', methods=['POST'])
def register():
    """添加用户"""
    result_dict = request.json
    job_number = result_dict['jobNumber']
    name = result_dict['name']
    password_hash = generate_password_hash(result_dict['password'])
    real_name = result_dict['realName']
    mobile = result_dict['mobile']
    role = result_dict['role']

    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', mobile):
        return jsonify(status=RET.PARAMERR, msg='请输入正确手机号码')

    try:
        sql = """
        insert into user (job_number, name, password_hash, real_name, mobile, role) values
        (%s, %s, %s, %s, %s, %s)
        """

        SqlHelper.execute(sql, [job_number, name, password_hash, real_name, mobile, role])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(status=RET.DATAEXIST, msg='账号已存在')

    return jsonify(status=RET.OK, msg='用户添加成功')


@api.route('/login', methods=['POST'])
def login():
    """处理用户登录操作"""
    result_dict = request.json
    name = result_dict['name']
    password = result_dict['password']

    if not all([name, password]):
        return jsonify(status=RET.PARAMERR, msg="缺少参数")

    has_user = SqlHelper.fetch_one('select * from user where name=%s', [name])
    password_hash = SqlHelper.fetch_one('select password_hash from user where name=%s', [name])

    if not has_user:
        return jsonify(status=RET.ACCOUNTERR, msg="用户不存在")

    if not check_password_hash(password_hash['password_hash'], password):
        return jsonify(status=RET.USERERR, msg="用户不存在或者密码错误")

    session['name'] = name

    return jsonify(status=RET.OK, msg="登录成功")


@api.route('/logout', methods=['DELETE'])
@login_require
def logout():
    """处理用户退出登录"""
    session.pop('name')

    return jsonify(status=RET.OK, msg='退出登录成功')


def generate_token(key, expire=86400):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


#  验证token 入参：用户id 和 token
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return False
    return True
