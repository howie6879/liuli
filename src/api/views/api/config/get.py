"""
    Created by howie.hu at 2023-03-27.
    Description: 获取 config 列表
    Changelog: all notable changes to this file will be documented
"""

import json

from bson import json_util
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
def config_get():
    """
    获取 config 列表
    eg:
    {
        "username": "liuli"
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_config")
    username = request.json["username"]

    db_res: dict = mongodb_find(
        coll_conn=coll,
        filter_dict={"config_flag": username},
        return_dict={"LL_JWT_SECRET_KEY": 0, "config_flag": 0, "_id": 0},
        sorted_list=[("updated_at", -1)],
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: db_res["info"][0] if db_res["info"] else {},
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
        result = json.loads(json_util.dumps(result))
    else:
        result = UniResponse.DB_ERR
        err_info = f"get liuli config failed! DB response info -> {db_res['info']}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
