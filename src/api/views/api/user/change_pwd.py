"""
    Created by howie.hu at 2023-03-26.
    Description: 修改用户密码
    Changelog: all notable changes to this file will be documented
"""

import time

from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_find, mongodb_update_data
from src.utils import md5_encryption


@jwt_required()
def user_change_pwd():
    """修改密码
    eg:
    {
        "username": "liuli",
        "o_password": "liuli",
        "n_password": "liuli"
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_user")
    # 获取基础数据
    post_data: dict = request.json
    username = post_data.get("username") or ""
    o_password = post_data.get("o_password") or ""
    n_password = post_data.get("n_password") or ""
    user_db_res = mongodb_find(
        coll_conn=coll,
        filter_dict={"username": username, "password": md5_encryption(o_password)},
        return_dict={"_id": 0},
    )
    user_info_list = user_db_res["info"]
    if username and n_password and user_db_res["status"] and len(user_info_list) == 1:
        # 历史用户存在
        db_res = mongodb_update_data(
            coll_conn=coll,
            filter_dict={"username": username},
            update_data={
                "$set": {
                    "password": md5_encryption(n_password),
                    "updated_at": int(time.time()),
                }
            },
        )
        if db_res["status"]:
            result = {
                ResponseField.DATA: {"username": username},
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            }

        else:
            result = UniResponse.CHANGE_PWD_ERROR
            err_info = f"change user pwd failed! DB response info -> {db_res['info']}"
            app_logger.error(err_info)

    else:
        result = UniResponse.CHANGE_PWD_ERROR
        err_info = f"change user pwd failed! DB response info -> {user_db_res}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
