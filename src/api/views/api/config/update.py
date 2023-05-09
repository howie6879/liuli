"""
    Created by howie.hu at 2023-03-27.
    Description: 更新 config 列表
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
from src.databases import MongodbBase, mongodb_update_data


@jwt_required()
def config_update():
    """
    获取 config 列表
    eg:
    {
        "username": "liuli",
        "data": {
            "LL_DEMO": "3"
        }
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_config")
    # 获取基础数据
    post_data: dict = request.json
    config_data = post_data.get("data", {})
    username = post_data["username"]

    db_res: dict = mongodb_update_data(
        coll_conn=coll,
        filter_dict={"config_flag": username},
        update_data={"$set": config_data},
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = f"update liuli config failed! DB response info -> {db_res['info']}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
