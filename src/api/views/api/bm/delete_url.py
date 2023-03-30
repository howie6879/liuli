"""
    Created by howie.hu at 2023-03-27.
    Description: 删除浏览器书签 url
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
from src.databases import MongodbBase, mongodb_delete_many_data


@jwt_required()
def bm_delete_url():
    """
    删除浏览器书签
    eg:
    {
        "url_list": ["https://github.com/howie6879/liuli"]
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll_bm = mongodb_base.get_collection(coll_name="liuli_bm")
    # 获取基础数据
    post_data: dict = request.json
    url_list = [url.strip() for url in post_data.get("url_list", [])]

    result = UniResponse.SUCCESS

    db_res: dict = mongodb_delete_many_data(coll_bm, {"url": {"$in": url_list}})

    if db_res["status"]:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = f"delete web bookmarket failed! DB response info -> {db_res['info']}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
