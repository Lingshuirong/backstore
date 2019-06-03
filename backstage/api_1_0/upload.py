from . import api
import os
import re
import base64
import random
import string
import time
import os
from flask import request, jsonify
from config import Config
from backstage.sql import SqlHelper
from backstage.utils.response_code import RET
from backstage.utils.common import certify_token


@api.route('/images/upload', methods=['POST'])
def upload():
    """上传图片"""

    token = request.headers.get('token')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    if not os.path.exists(Config.FILE_PATH):
        os.makedirs(Config.FILE_PATH)

    result_dict = request.json
    data = result_dict['data']
    name = data[0]['name']

    temp_lsit = data[0]['thumbUrl'].split(',')
    img_data = base64.b64decode(temp_lsit[1])
    # img_formate = re.findall(r'/(.*);', temp_lsit[0])[0]

    with open(Config.FILE_PATH + name, 'wb') as f:
        f.write(img_data)

    sql = "insert into sys_info (qr_url) values (%s) "
    SqlHelper.execute(sql, [name])

    return jsonify(status=RET.OK, msg="图片上传成功")


@api.route('/change/image', methods=['GET', 'DELETE'])
def get_img():
    """系统设置页面获取图片"""
    if request.method == 'GET':
        file_list = SqlHelper.fetch_all('select qr_url from sys_info')[0]
        img_content_list = []
        for file in file_list:
            temp_dict = {}
            temp_dict['name'] = file['qr_url']
            temp_dict['content'] = get_img_content(file['qr_url'])
            img_content_list.append(temp_dict)
        return jsonify(img_list=img_content_list, status=RET.OK)
    elif request.method == 'DELETE':
        name = request.args.get('name')
        SqlHelper.execute('delete from sys_info where qr_url=%s', [name])
        try:
            os.remove(Config.FILE_PATH + name)
        except Exception:
            pass
        return jsonify(status=RET.OK, msg='删除成功')


def get_img_content(file):
    with open(Config.FILE_PATH + file, 'rb') as f:
        content = f.read()
    b64_content = base64.b64encode(content)

    return b64_content.decode()



