import base64
import time
import hmac
import re
from flask import request, session, g, current_app, jsonify, make_response
from . import api
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.common import login_require, admin_require


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
    reg_time = time.strftime('%Y-%m-%d %H:%M:%S')

    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', mobile):
        return jsonify(status=RET.PARAMERR, msg='请输入正确手机号码')

    try:
        sql = """
        insert into user (job_number, name, password_hash, real_name, mobile, role, reg_time) values
        (%s, %s, %s, %s, %s, %s, %s)
        """

        SqlHelper.execute(sql, [job_number, name, password_hash, real_name, mobile, role, reg_time])
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
    token = generate_token(name)

    user_info = SqlHelper.fetch_one("select * from user where name=%s", [name])

    if has_user['role'] == '管理员':
        response = jsonify(status=RET.OK, msg='登录成功', name=name, permission=True, token=token,
                           mobile=user_info['mobile'], jobNumber=user_info['job_number'], realName=user_info['real_name'])
        # response.set_cookie('name', name, max_age=86400)
        return response

    response = jsonify(status=RET.OK, msg="登录成功", name=name, permission=False, token=token,
                       mobile=user_info['mobile'], jobNumber=user_info['job_number'], realName=user_info['real_name'])

    return response


@api.route('/logout', methods=['DELETE'])
@login_require
def logout():
    """处理用户退出登录"""
    session.pop('name')

    return jsonify(status=RET.OK, msg='退出登录成功')


@api.route('/change/password', methods=['POST'])
@login_require
@admin_require
def change_info():
    """修改用户信息"""
    result_dict = request.json
    name = result_dict['name']
    old_password = result_dict['oldPassword']
    new_password = result_dict['newPassword']
    confirm_password = result_dict['confirmPassword']

    password_hash = generate_password_hash(new_password)
    sql = "update user set password_hash=%s where name=%s"
    SqlHelper.execute(sql, [password_hash, name])

    return jsonify(status=RET.OK, msg='密码修改成功')


@api.route('/profile', methods=['POST'])
@login_require
def profile():
    """查询用户资料"""
    result_dict = request.json
    name = result_dict['name']
    sql = "select * from user where name=%s"
    result = SqlHelper.fetch_one(sql, [name])
    return jsonify(name=result['name'], jobNumber=result['job_number'], realName=result['real_name'],
                   mobile=result['mobile'], idCardNumber=result['id_card_number'])


@api.route('/user/all', methods=['POST'])
@login_require
@admin_require
def user_list():
    """获取用户列表"""
    result_dict = request.json
    name = result_dict['name']
    real_name = result_dict['realName']
    role = result_dict['role']
    sql = "select * from user where "
    if name:
        sql = sql + f" name=\'{name}\' " + " and "

    if real_name:
        sql = sql + f" real_name=\'{real_name}\' " + " and "

    if role and role != '全部':
        sql = sql + f" role=\'{role}\' "
    else:
        sql = sql[:-4]

    result_list = SqlHelper.fetch_all(sql=sql)
    temp_list = []
    for result in result_list:
        temp_dict = {}
        temp_dict['regTime'] = result['reg_time']
        temp_dict['name'] = result['name']
        temp_dict['jobNumber'] = result['job_number']
        temp_dict['realName'] = result['real_name']
        temp_dict['mobile'] = result['mobile']
        temp_dict['role'] = result['role']
        temp_list.append(temp_dict)

    return make_response(jsonify(userList=temp_list))


@api.route('/change/user', methods=['POST'])
@login_require
def change_user():
    """修改用户"""
    pass


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

