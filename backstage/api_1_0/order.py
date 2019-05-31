import re
from . import api
from flask import request, jsonify
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from datetime import datetime


@api.route('/order', methods=['POST', 'GET'])
def order():
    """订单处理"""

    if request.method == 'POST':
        result_dict = request.json
        job_number = str(result_dict['referralNum'])
        bank_card = result_dict['bankCard']
        pre_paid = int(result_dict['prestore'])
        name = result_dict['name']
        id_card_number = result_dict['card']
        mobile = result_dict['phone']

        # 判断用户是否已经存在未支付订单
        status_list = SqlHelper.fetch_all('select paid_status from order_tb where id_card_number=%s', [id_card_number])
        if status_list:
            temp_list = []
            for status in status_list:
                temp_list.append(status['paid_status'])

            if '待支付' in temp_list:
                return jsonify(status=RET.ORDERERR, msg="请勿重复提交。如果已支付完成，工作人员将会联系您！")

        sql = "insert into order_tb (recommand_job_number, name, id_card_number, mobile, bank_card_number, pre_paid_amnount," \
              " commit_datetime, update_datetime) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s)"
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SqlHelper.execute(sql, [job_number, name, id_card_number, mobile, bank_card, pre_paid, date, date])
        return jsonify(status=RET.OK, msg='订单提交成功')
    elif request.method == 'GET':
        job_number = request.args.get('referralNum')
        result = SqlHelper.fetch_one('select * from user where job_number=%s', [job_number])
        if result:
            return jsonify(status=RET.OK, msg='欢迎')
        else:
            return jsonify(status=RET.DATAEXIST, msg='工号不存在,请重新输入')


@api.route('/order_list', methods=['POST'])
def order_list():
    result_dict = request.json
    job_number = result_dict['job']
    status = result_dict['status']
    s_date = result_dict['sDate']
    e_date = result_dict['eDate']
    name_or_mobile = result_dict['search_info']
    page = int(result_dict['page'])
    rows = int(result_dict['rows'])

    sql = """
        select commit_datetime, name, id_card_number, bank_number, mobile, job_number, pre_paid_amount, paid_status 
        from order_tb where 
    """

    if job_number:
        sql = sql + f" job_number=\'{job_number}\'" + " and "

    if status:
        sql = sql + f" paid_status=\'{status}\'" + " and "

    if s_date and e_date:
        sql = sql + f" commit_datetime between \'{s_date}\' and \'{e_date}\' " + " and "

    if name_or_mobile:
        sql = sql + f" name like \'%{name_or_mobile}\'% or \'%{name_or_mobile}%\' "
    else:
        sql = sql[:-4]

    page = (page - 1) * rows
    sql = sql + f" limit {page},{rows}"

    result_list = SqlHelper.fetch_all(sql)
    data_list = []
    for result in result_list:
        temp_dict = {}
        temp_dict['commitDatetime'] = result['commit_datetime']
        temp_dict['name'] = result['name']
        temp_dict['idCardNumber'] = result['id_card_number']
        temp_dict['bankNumber'] = result['bank_number']
        temp_dict['mobile'] = result['mobile']
        temp_dict['jobNumber'] = result['job_number']
        temp_dict['prePaidAmount'] = result['pre_paid_amount']
        temp_dict['paidStatus'] = result['paid_status']
        data_list.append(temp_dict)

    return jsonify(info_list=data_list)




