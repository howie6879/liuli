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

    BM_URL_IS_EMPTY = "书签URL为空"
    BM_URL_TAG_IS_EMPTY = "书签URL&Tag为空"
    USER_LOGIN_ERROR = "用户登录失败"
    USER_CHANGE_PWD_ERROR = "用户修改密码失败"
    NOT_AUTHORIZED = "验证未通过"
    GEN_RSS_FAILED = "RSS 生成失败"
    GEN_BACKUP_FAILED = "BACKUP 生成失败"
    GET_DC_EMPTY = "获取不到 doc_source 配置"
    NOT_READY = "服务尚未准备就绪"
    GET_DOC_EMPTY = "获取不到 doc_id 相关文章"

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
    BM_URL_IS_EMPTY = 800
    BM_URL_TAG_IS_EMPTY = 801
    USER_LOGIN_ERROR = 901
    USER_CHANGE_PWD_ERROR = 902
    GEN_RSS_FAILED = 903
    GEN_BACKUP_FAILED = 904
    GET_DC_EMPTY = 905
    NOT_READY = 906
    GET_DOC_EMPTY = 907


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
    # 服务尚未准备就绪
    NOT_READY = {
        ResponseField.DATA: {},
        ResponseField.MESSAGE: ResponseReply.NOT_READY,
        ResponseField.STATUS: ResponseCode.NOT_READY,
    }


if __name__ == "__main__":
    print(UniResponse().SUCCESS)
