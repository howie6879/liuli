"""
    Created by howie.hu at 2023-03-27.
    Description: 删除 config 字段
    Changelog: all notable changes to this file will be documented
"""

from bson import ObjectId
from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_update_data


@jwt_required()
def config_delete():
    """
    删除 config
    eg:
    {
        "username": "liuli",
        "_id": "64215cca554b6d873380103a",
        "config_key": ["LL_DEMO", "LL_HELLO"]
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_config")
    # 获取基础数据
    post_data: dict = request.json
    _id = post_data["_id"]
    config_key = post_data.get("config_key", [])

    if config_key:
        result = UniResponse.SUCCESS
        unset_dict = {}
        for each in config_key:
            unset_dict[each] = 1

        u_db_res: dict = mongodb_update_data(
            coll_conn=coll,
            filter_dict={"_id": ObjectId(_id)},
            update_data={"$unset": unset_dict},
        )

        if u_db_res["status"]:
            result = {
                ResponseField.DATA: {},
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            }
        else:
            result = UniResponse.DB_ERR
            err_info = (
                f"update liuli config failed! DB response info -> {u_db_res['info']}"
            )
            app_logger.error(err_info)
    else:
        result = UniResponse.DB_ERR
        err_info = "delete liuli config failed! DB response info -> config_key is not expert empty!"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
