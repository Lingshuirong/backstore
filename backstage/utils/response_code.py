# coding:utf-8

class RET(object):
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"
    FORMATERR = "4502"
    ACCOUNTERR = "4503"
    PERMISSIONERR = "4504"
    ORDERERR = "4505"


error_map = {
    RET.OK: "成功",
    RET.DBERR: "数据库查询错误",
    RET.NODATA: "无数据",
    RET.DATAEXIST: "数据已存在",
    RET.DATAERR: "数据错误",
    RET.SESSIONERR: "用户未登录",
    RET.LOGINERR: "用户登录失败",
    RET.PARAMERR: "参数错误",
    RET.USERERR: "用户不存在或未激活",
    RET.ROLEERR: "用户身份错误",
    RET.PWDERR: "用户或密码错误",
    RET.REQERR: "非法请求或请求次数受限",
    RET.IPERR: "IP受限",
    RET.THIRDERR: "第三方系统错误",
    RET.IOERR: "文件读写错误",
    RET.SERVERERR: "内部错误",
    RET.UNKOWNERR: "未知错误",
    RET.FORMATERR: "邮箱格式错误",
    RET.ACCOUNTERR: "账号不存在",
    RET.PERMISSIONERR: "权限不足",
    RET.ORDERERR: "订单提交错误"
}
