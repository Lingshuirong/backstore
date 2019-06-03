import time
import re
from flask import request, session, jsonify, make_response
from . import api
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.common import generate_token, login_require, certify_token


@api.route('/register', methods=['POST'])
def register():
    """添加用户"""
    result_dict = request.json
    cookie = request.headers.get('token')
    job_number = result_dict['jobNumber']
    name = result_dict['name']
    password_hash = generate_password_hash(result_dict['password'])
    real_name = result_dict['realName']
    mobile = result_dict['mobile']
    role = result_dict['role']
    reg_time = time.strftime('%Y-%m-%d %H:%M:%S')

    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', mobile):
        return jsonify(status=RET.PARAMERR, msg='请输入正确手机号码')

    sql = """
    insert into user (job_number, name, password_hash, real_name, mobile, role, reg_time) values
    (%s, %s, %s, %s, %s, %s, %s)
    """

    status = SqlHelper.execute(sql, [job_number, name, password_hash, real_name, mobile, role, reg_time])
    if status:
        return jsonify(status=RET.OK, msg='用户添加成功')
    else:
        return jsonify(status=RET.DATAEXIST, msg='账号已存在')


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
                           mobile=user_info['mobile'], jobNumber=user_info['job_number'],
                           realName=user_info['real_name'], uid=user_info['id'])
        return response

    response = jsonify(status=RET.OK, msg="登录成功", name=name, permission=False, token=token,
                       mobile=user_info['mobile'], jobNumber=user_info['job_number'], realName=user_info['real_name'],
                       uid=user_info['id']
                       )

    return response


@api.route('/logout', methods=['DELETE'])
def logout():
    """处理用户退出登录"""
    session.pop('name')

    return jsonify(status=RET.OK, msg='退出登录成功')


@api.route('/change/password', methods=['POST'])
def change_info():
    """修改用户信息"""
    result_dict = request.json
    token = request.headers.get('token')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    name = result_dict['name']
    old_password = result_dict['oldPassword']
    new_password = result_dict['newPassword']
    confirm_password = result_dict['confirmPassword']

    result = SqlHelper.execute('select password_hash from user where name=%s', [name])
    if not result:
        return jsonify(status=RET.DATAERR, msg='用户不存在')
    else:
        if not check_password_hash(result['password_hash'], old_password):
            return jsonify(status=RET.PWDERR, msg='旧密码不正确,请重新输入')

    password_hash = generate_password_hash(new_password)
    sql = "update user set password_hash=%s where name=%s"
    SqlHelper.execute(sql, [password_hash, name])

    return jsonify(status=RET.OK, msg='密码修改成功')


@api.route('/profile', methods=['POST'])
def profile():
    """查询用户资料"""
    result_dict = request.json
    token = request.headers.get('token', '')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    name = result_dict['name']
    sql = "select * from user where name=%s"
    result = SqlHelper.fetch_one(sql, [name])
    if result:
        return jsonify(name=result['name'], jobNumber=result['job_number'], realName=result['real_name'],
                       mobile=result['mobile'], idCardNumber=result['id_card_number'])
    else:
        return jsonify(status=RET.DBERR, msg='查询用户资料出错')


@api.route('/user/all', methods=['POST'])
def user_list():
    """获取用户列表"""
    result_dict = request.json
    token = request.headers.get('token', '')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    name = result_dict['name']
    real_name = result_dict['realName']
    role = result_dict['role']
    page = result_dict['page']
    rows = result_dict['rows']
    page = (page - 1) * rows

    if not any([name, real_name, role]):
        sql = f"SELECT sql_calc_found_rows name, job_number, real_name, mobile, role, reg_time, id FROM  user limit {page}, {rows}"

    else:
        sql = "select sql_calc_found_rows name, job_number, real_name, mobile, role, reg_time, id from user where "
        if name:
            sql = sql + f" name like \'%{name}%\' " + " and "

        if real_name:
            sql = sql + f" real_name like \'%{real_name}%\' " + " and "

        if role and role != '全部':
            sql = sql + f" role=\'{role}\' "
        else:
            sql = sql[:-4]

        sql = sql + f' limit {page}, {rows}'

    result_list, total = SqlHelper.fetch_all(sql=sql)
    temp_list = []
    if result_list:
        for result in result_list:
            temp_dict = {}
            temp_dict['regTime'] = result['reg_time']
            temp_dict['name'] = result['name']
            temp_dict['jobNumber'] = result['job_number']
            temp_dict['realName'] = result['real_name']
            temp_dict['mobile'] = result['mobile']
            temp_dict['role'] = result['role']
            temp_dict['id'] = result['id']
            temp_list.append(temp_dict)
    else:
        temp_list = None

    return make_response(jsonify(userList=temp_list, status=0, total=total['total']))


@api.route('/change/user', methods=['POST', 'DELETE'])
def change_user():
    """修改用户"""

    token = request.headers.get('token', '')
    if request.method == 'DELETE':

        name = request.args.get('name')

        if token:
            if not certify_token(token):
                return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
        else:
            return jsonify(status=RET.PERMISSIONERR, msg='无效口令')

        SqlHelper.execute("delete from user where name=%s ", [name])

        return jsonify(status=RET.OK, msg="删除用户成功")
    else:
        result_dict = request.json
        name = result_dict['name']
        job_number = result_dict['jobNumber']
        role = result_dict['role']
        real_name = result_dict['realName']
        mobile = result_dict['obile']
        password = result_dict['password']
        user_id = result_dict['id']
        sql = "update user set name=%s, password_hash=%s, job_number%s, real_name=%s, mobile=%s, role=%s where id=%s"
        SqlHelper.execute(sql, [name, generate_password_hash(password), job_number, real_name, mobile, role, user_id])
        return jsonify(status=RET.OK, msg="修改用户信息成功")