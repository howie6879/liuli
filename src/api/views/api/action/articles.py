"""
    Created by howie.hu at 2023-03-26.
    Description: 查询历史文章
    Changelog: all notable changes to this file will be documented
"""
import json

from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_find_by_page


@jwt_required()
def action_articles():
    """查询历史文章
    {
        "username": "liuli",
        "doc_source": "liuli_wechat",
        "doc_source_name": "",
        "size": 10,
        "page": 1,
        "sorted_order": 1
    }

    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_articles")
    # 获取基础数据
    post_data: dict = request.json
    doc_source = post_data.get("doc_source", "")
    doc_source_name = post_data.get("doc_source_name", "")
    size = post_data.get("size", 10)
    page = post_data.get("page", 1)
    filter_dict = {"doc_source": doc_source} if doc_source else {}
    if doc_source_name:
        filter_dict.update({"doc_source_name": doc_source_name})
    db_res = mongodb_find_by_page(
        coll_conn=coll,
        filter_dict=filter_dict,
        size=size,
        page=page,
        return_dict={"doc_content": 0, "doc_core_html": 0, "doc_html": 0},
        sorted_list=[("doc_ts", post_data.get("sorted_order", -1))],
    )
    db_info = db_res["info"]
    if db_res["status"]:
        # 对于 _id 做强制 str 处理
        return json.dumps(
            {
                ResponseField.DATA: {**db_info, **{"size": size, "page": page}},
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            },
            default=str,
        )
    else:
        result = UniResponse.DB_ERR
        err_info = f"query doc articles failed! DB response info -> {db_info}"
        app_logger.error(err_info)

        return response_handle(request=request, dict_value=result)
