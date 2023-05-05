"""
    Created by howie.hu at 2023-05-05.
    Description: 根据 doc_id 获取详情
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
from src.utils.tools import text_decompress


@jwt_required()
def articles_get():
    """根据 doc_id 获取详情
    eg:
    {
        "username": "liuli",
        "doc_id": ""
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_articles")
    # 获取基础数据
    post_data: dict = request.json
    doc_id = post_data.get("doc_id", "")

    db_res = mongodb_find(
        coll_conn=coll, filter_dict={"doc_id": doc_id}, return_dict={"_id": 0}, limit=1
    )
    db_info = db_res["info"]
    if db_res["status"]:
        if db_info:
            final_data = db_info[0]
            final_data["doc_core_html"] = text_decompress(final_data["doc_core_html"])
            result = {
                ResponseField.DATA: final_data,
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            }
        else:
            result = {
                ResponseField.DATA: {},
                ResponseField.MESSAGE: ResponseReply.GET_DOC_EMPTY,
                ResponseField.STATUS: ResponseCode.GET_DOC_EMPTY,
            }

    else:
        result = UniResponse.DB_ERR
        err_info = f"get doc failed! DB response info -> {db_info}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
