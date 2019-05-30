import re
from . import api
from flask import request, jsonify
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from datetime import datetime


@api.route('/order', methods=['POST'])
def order():
    """订单处理"""

    result_dict = request.json
    job_number = result_dict['jobNumber']
    name = result_dict['name']
    id_card_number = result_dict['idCardNumber']
    mobile = result_dict['mobile']

    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', mobile):
        return jsonify(status=RET.PARAMERR, msg='请输入正确的手机号')

    if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$ '
                    r'| ^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$', id_card_number):
        return jsonify(status=RET.PARAMERR, msg='请输入正确的身份证号码')

    sql = "insert into order_tb (recommand_job_number, name, id_card_number, mobile, commit_datetime, update_datetime) " \
          "values (%s, %s, %s, %s, %s, %s)"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    SqlHelper.execute(sql, [job_number, name, id_card_number, mobile, date, date])
    return jsonify(status=RET.OK, msg='信息提交成功')


@api.route('/payment', methods=['POST'])
def bank():
    result_dict = request.json
    name = result_dict['name']
    id_card_number = result_dict['idCardNumber']
    mobile = result_dict['mobile']
    bank_number = result_dict['bank_number']
    amount = result_dict['amount']

    return jsonify(status=RET.OK, msg="提交成功")
