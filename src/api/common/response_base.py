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

    # Success
    SUCCESS = "ok"


class ResponseCode:
    """
    定义通用响应状态码
    """

    BAD_REQUEST = 400
    SERVER_ERR = 500
    SUCCESS = 200


class UniResponse:
    """
    通用响应字典
    """

    # 数据库出错
    DB_ERR = {
        ResponseField.MESSAGE: ResponseReply.DB_ERROR,
        ResponseField.STATUS: ResponseCode.SERVER_ERR,
        ResponseField.DATA: {},
    }
    # 参数错误
    PARAM_ERR = {
        ResponseField.MESSAGE: ResponseReply.PARAM_ERR,
        ResponseField.STATUS: ResponseCode.BAD_REQUEST,
        ResponseField.DATA: {},
    }
    # 服务未知错误
    SERVER_UNKNOWN_ERR = {
        ResponseField.MESSAGE: ResponseReply.UNKNOWN_ERR,
        ResponseField.STATUS: ResponseCode.SERVER_ERR,
        ResponseField.DATA: {},
    }
    # 请求成功
    SUCCESS = {
        ResponseField.MESSAGE: ResponseReply.SUCCESS,
        ResponseField.STATUS: ResponseCode.SUCCESS,
        ResponseField.DATA: {},
    }
