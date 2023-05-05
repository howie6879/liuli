"""
    Created by howie.hu at 2023-05-05.
    Description: 文档搜索接口
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
from src.databases import MongodbBase, mongodb_find_by_page


@jwt_required()
def articles_search():
    """获取 文章
    eg:
    {
        "username": "liuli",
        "doc_source": "wechat",
        "doc_source_name": "",
        "doc_name":"老胡的周刊（第089期）",
        "doc_type": "",
        "page": 1,
        "page_size": 2
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_articles")
    # 获取基础数据
    post_data: dict = request.json
    doc_type = post_data.get("doc_type", "")
    doc_source = post_data.get("doc_source", "")
    doc_source_name = post_data.get("doc_source_name", "")
    doc_name = post_data.get("doc_name", "")
    page = post_data.get("page", 1)
    page_size = post_data.get("page_size", 20)

    filter_dict = {}

    if doc_source:
        filter_dict["doc_source"] = doc_source
    if doc_source_name:
        filter_dict["doc_source_name"] = {"$regex": doc_source_name, "$options": "$i"}
    if doc_name:
        filter_dict["doc_name"] = doc_name
    if doc_type:
        filter_dict["doc_type"] = doc_type

    result = UniResponse.SUCCESS

    db_res: dict = mongodb_find_by_page(
        coll_conn=coll,
        filter_dict=filter_dict,
        size=page_size,
        page=page,
        return_dict={"_id": 0, "doc_content": 0, "doc_core_html": 0},
        sorted_list=[("doc_ts", -1)],
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: db_res["info"],
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = f"search articles failed! DB response info -> {db_res['info']}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
