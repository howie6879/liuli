"""
    Created by howie.hu at 2023-03-27.
    Description: 获取 favorite 列表
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
from src.databases import MongodbBase


@jwt_required()
def favorite_get():
    """
    获取 favorite 列表
    eg:
    {
        "username": "liuli",
        "page": 1,
        "page_size": 2
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_favorite")
    username = request.json["username"]
    post_data: dict = request.json
    page = post_data.get("page", 1)
    page_size = post_data.get("page_size", 20)
    try:
        db_res = coll.aggregate(
            [
                {"$match": {"username": username}},
                {
                    "$lookup": {
                        "from": "liuli_articles",
                        "localField": "doc_id",
                        "foreignField": "doc_id",
                        "as": "doc",
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "doc": {"_id": 0, "doc_core_html": 0, "doc_content": 0},
                    }
                },
                {"$skip": (page - 1) * page_size},
                {"$limit": page_size},
            ]
        )
        db_res_list = list(db_res)
        result = {
            ResponseField.DATA: {"rows": db_res_list, "total": len(db_res_list)},
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    except Exception as e:
        result = UniResponse.DB_ERR
        err_info = f"search user favorite doc failed! DB response info -> {e}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
