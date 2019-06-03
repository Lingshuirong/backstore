from . import api
from flask import request, jsonify
from backstage.utils.response_code import RET
from backstage.sql import SqlHelper
from datetime import datetime
from backstage.utils.common import certify_token


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
                return jsonify(status=RET.ORDERERR, msg="请勿重复提交。如已支付,工作人员将会联系您!")

        sql = "insert into order_tb (recommand_job_number, name, id_card_number, mobile, bank_card_number, pre_paid_amnount," \
              " commit_datetime, update_datetime) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s)"
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = SqlHelper.execute(sql, [job_number, name, id_card_number, mobile, bank_card, pre_paid, date, date])
        if status:
            return jsonify(status=RET.OK, msg='订单提交成功')
        else:
            return jsonify(status=RET.DBERR, msg="订单提交失败,请重新提交")
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
    token = request.headers.get('token', '')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    job_number = result_dict.get('jobNumber', '')
    status = result_dict['status']
    s_date = result_dict['sDate']
    e_date = result_dict['eDate']
    name_or_mobile = result_dict['search_info']
    page = int(result_dict['page'])
    rows = int(result_dict['rows'])

    if not any([job_number, status, s_date, e_date, name_or_mobile]):
        sql = """
            select sql_calc_found_rows id, commit_datetime, name, id_card_number, bank_card_number, mobile, recommand_job_number, pre_paid_amount, 
            paid_status from order_tb
        """
    else:

        sql = """
            select sql_calc_found_rows id, commit_datetime, name, id_card_number, bank_card_number, mobile, recommand_job_number, 
            pre_paid_amount, paid_status from order_tb where
        """

        if job_number:
            sql = sql + f" recommand_job_number=\'{job_number}\'" + " and "

        if status:
            sql = sql + f" paid_status=\'{status}\'" + " and "

        if s_date and e_date:
            sql = sql + f" commit_datetime between \'{s_date} 00:00:00\' and \'{e_date} 23:59:59\' " + " and "

        if name_or_mobile:
            sql = sql + f" name like \'%{name_or_mobile}%\' or mobile like \'%{name_or_mobile}%\' "
        else:
            sql = sql[:-4]

    page = (page - 1) * rows
    sql = sql + f" limit {page},{rows}"

    result_list, total = SqlHelper.fetch_all(sql=sql)
    data_list = []
    if result_list:
        for result in result_list:
            temp_dict = {}
            temp_dict['commitDatetime'] = result['commit_datetime']
            temp_dict['name'] = result['name']
            temp_dict['idCardNumber'] = result['id_card_number']
            temp_dict['bankNumber'] = result['bank_card_number']
            temp_dict['mobile'] = result['mobile']
            temp_dict['jobNumber'] = result['recommand_job_number']
            temp_dict['prePaidAmount'] = result['pre_paid_amount']
            temp_dict['paidStatus'] = result['paid_status']
            temp_dict['orderId'] = result['id']
            data_list.append(temp_dict)
    else:
        data_list = None

    return jsonify(info_list=data_list, status=RET.OK, total=total['total'])


@api.route('/order/update', methods=['POST'])
def update_order():
    """更新订单状态"""

    result_dict = request.json
    token = request.headers.get('token', '')
    if token:
        if not certify_token(token):
            return jsonify(status=RET.PERMISSIONERR, msg='超时登录')
    else:
        return jsonify(status=RET.PERMISSIONERR, msg='无效口令')
    order_id = result_dict['orderId']
    sql = "update order_tb set paid_status=%s where id=%s"
    SqlHelper.execute(sql, ['已支付', order_id])
    return jsonify(status=RET.OK, msg='订单状态更新')
