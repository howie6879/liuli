"""
    Created by howie.hu at 2023-03-27.
    Description: 获取 tag 列表
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
def bm_get_tag_list():
    """
    获取 tag 列表
    eg:
    {
        "tag": ""
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll_bm = mongodb_base.get_collection(coll_name="liuli_bm_tags")
    # 获取基础数据
    post_data: dict = request.json
    tag = post_data.get("tag", "").strip()

    db_res: dict = mongodb_find(
        coll_conn=coll_bm,
        filter_dict={"tag": {"$regex": tag, "$options": "$i"}},
        return_dict={"_id": 0},
        sorted_list=[("updated_at", -1)],
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: db_res["info"],
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = (
            f"get web bookmarket tag list failed! DB response info -> {db_res['info']}"
        )
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
