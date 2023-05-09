"""
    Created by howie.hu at 2023-05-05.
    Description: 收藏喜欢 doc_id
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


@jwt_required()
def favorite_article():
    """收藏喜欢 doc_id
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
    coll = mongodb_base.get_collection(coll_name="liuli_favorite")
    article_oll = mongodb_base.get_collection(coll_name="liuli_articles")
    # 获取基础数据
    post_data: dict = request.json
    username = post_data.get("username", "")
    doc_id = post_data.get("doc_id", "")

    result = UniResponse.SUCCESS

    db_res = mongodb_find(
        coll_conn=article_oll,
        filter_dict={"doc_id": doc_id},
        return_dict={"_id": 0},
        limit=1,
    )
    db_info = db_res["info"]
    if db_res["status"]:
        if db_info:
            db_res = mongodb_update_data(
                coll_conn=coll,
                filter_dict={"username": username, "doc_id": doc_id},
                update_data={
                    "$set": {
                        "doc_id": doc_id,
                        "username": username,
                        "updated_at": int(time.time()),
                        "source_db": "liuli_articles",
                    }
                },
            )

            if not db_res["status"]:
                # 更新失败
                result = UniResponse.DB_ERR
                err_info = (
                    f"Add favorite doc failed! DB response info -> {db_res['info']}"
                )
                app_logger.error(err_info)
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
