from . import api
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
from backstage.utils.common import login_require


@api.route('/images/uploaded', methods=['POST'])
def upload():
    """上传图片"""

    token = request.cookies.get('token', '')
    login_require(token)
    if os.path.exists(Config.FILE_PATH):
        os.makedirs(Config.FILE_PATH)

    url_list = []
    result_dict = request.json
    name = result_dict['name']
    temp_lsit = result_dict['data'].split(',')
    img_data = base64.b64decode(temp_lsit[1])
    img_formate = re.findall(r'/(.*);', temp_lsit[0])[0]
    img_name = Config.FILE_PATH + "".join(random.sample(string.ascii_letters + string.digits, 16)) \
               + str(int(time.time() * 1000)) + "." + img_formate

    url_list.append(img_name)

    with open(img_name, 'wb') as f:
        f.write(img_data)

    img_url_str = ";".join(url_list)
    sql = "insert into sys_info (user_id, qr_url) values (%s, %s) "
    SqlHelper.execute(sql, [name, img_url_str])

    return jsonify(status=RET.OK, msg="图片上传成功")


@api.route('/images/query')
def get_img():
    """系统设置页面获取图片"""
    pass
