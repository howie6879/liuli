"""
    Created by howie.hu at 2023-03-26.
    Description: 获取 doc_source
    Changelog: all notable changes to this file will be documented
"""


from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_find


@jwt_required()
def doc_source_get():
    """获取 doc_source
    eg:
    {
        "username": "liuli",
        "doc_source": "wechat"
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_doc_source")
    # 获取基础数据
    post_data: dict = request.json
    doc_source = post_data.get("doc_source", "")
    username = post_data.get("username", "")
    filter_dict = {"username": username}
    if doc_source:
        filter_dict["doc_source"] = doc_source
    db_res = mongodb_find(
        coll_conn=coll,
        filter_dict=filter_dict,
        return_dict={"_id": 0},
        sorted_list=[("doc_source", -1)],
    )
    db_info = db_res["info"]
    if db_res["status"]:
        if db_info:
            result = {
                ResponseField.DATA: db_info,
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            }
        else:
            result = {
                ResponseField.DATA: "",
                ResponseField.MESSAGE: ResponseReply.GET_DC_EMPTY,
                ResponseField.STATUS: ResponseCode.GET_DC_EMPTY,
            }

    else:
        result = UniResponse.DB_ERR
        err_info = f"get doc source config failed! DB response info -> {db_info}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
