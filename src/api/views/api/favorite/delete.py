"""
    Created by howie.hu at 2023-05-09.
    Description: 删除喜欢的资源
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
def favorite_delete():
    """
    删除喜欢的资源
    eg:
    {
        "doc_id_list": [""]
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_favorite")
    username = request.json["username"]
    post_data: dict = request.json

    doc_id_list: list = post_data.get("doc_id_list", [])

    db_res: dict = mongodb_delete_many_data(
        coll, {"doc_id": {"$in": doc_id_list}, "username": username}
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = (
            f"delete favorite doc id failed! DB response info -> {db_res['info']}"
        )
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
