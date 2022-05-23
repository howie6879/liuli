"""
    Created by howie.hu at 2022-02-11.
    Description: 常用状态码
    Changelog: all notable changes to this file will be documented
"""


class ResponseField:
    """
    定义通用响应字段
    """

    DATA = "data"
    MESSAGE = "info"
    STATUS = "status"


class ResponseReply:
    """
    定义通用描述
    """

    # Error
    DB_ERROR = "数据库操作错误"
    PARAM_ERR = "参数错误!"
    PARAM_PARSE_ERR = "参数解析错误!"
    UNKNOWN_ERR = "未知错误"
    USER_LOGIN_ERROR = "用户登录失败"
    USER_CHANGE_PWD_ERROR = "用户修改密码失败"
    NOT_AUTHORIZED = "验证未通过"

    # Success
    SUCCESS = "ok"


class ResponseCode:
    """
    定义通用响应状态码
    """

    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_AUTHORIZED = 401
    SERVER_ERR = 500
    USER_LOGIN_ERROR = 901
    USER_CHANGE_PWD_ERROR = 902


class UniResponse:
    """
    通用响应字典
    """

    # 数据库出错
    DB_ERR = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.DB_ERROR,
        ResponseField.STATUS: ResponseCode.SERVER_ERR,
    }
    # 参数错误
    PARAM_ERR = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.PARAM_ERR,
        ResponseField.STATUS: ResponseCode.BAD_REQUEST,
    }
    # 服务未知错误
    SERVER_UNKNOWN_ERR = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.UNKNOWN_ERR,
        ResponseField.STATUS: ResponseCode.SERVER_ERR,
    }
    # 请求成功
    SUCCESS = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.SUCCESS,
        ResponseField.STATUS: ResponseCode.SUCCESS,
    }
    # 未验证
    NOT_AUTHORIZED = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.NOT_AUTHORIZED,
        ResponseField.STATUS: ResponseCode.NOT_AUTHORIZED,
    }
    # 修改密码失败
    CHANGE_PWD_ERROR = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.USER_CHANGE_PWD_ERROR,
        ResponseField.STATUS: ResponseCode.USER_CHANGE_PWD_ERROR,
    }
