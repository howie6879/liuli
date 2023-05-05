"""
    Created by howie.hu at 2023-03-27.
    Description: 查询书签
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
def bm_search():
    """
    查询浏览器书签
    eg:
    {
        "url": "https://github.com/howie6879/liuli",
        "tags": ["1", "2"],
        "title": "title",
        "des": "des",
        "page": 1,
        "page_size": 2
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll_bm = mongodb_base.get_collection(coll_name="liuli_bm")
    # 获取基础数据
    post_data: dict = request.json
    url = post_data.get("url", "").strip()
    # 全部小写去空格
    tags = [str(i).lower().strip() for i in post_data.get("tags", [])]
    title = post_data.get("title", "")
    des = post_data.get("des", "")

    # 分页限制
    page = post_data.get("page", 1)
    page_size = post_data.get("page_size", 10)

    filter_dict = {}

    if tags:
        filter_dict["tags"] = {"$elemMatch": {"$in": tags}}

    if url or title or des:
        filter_dict = {"$or": []}
        if url:
            filter_dict["$or"].append({"url": {"$regex": url, "$options": "$i"}})
        if title:
            filter_dict["$or"].append({"title": {"$regex": title, "$options": "$i"}})
        if des:
            filter_dict["$or"].append({"des": {"$regex": des, "$options": "$i"}})

    result = UniResponse.SUCCESS

    db_res: dict = mongodb_find_by_page(
        coll_conn=coll_bm,
        filter_dict=filter_dict,
        size=page_size,
        page=page,
        return_dict={"_id": 0},
        sorted_list=[("updated_at", 1)],
    )

    if db_res["status"]:
        result = {
            ResponseField.DATA: db_res["info"],
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.DB_ERR
        err_info = f"search web bookmarket failed! DB response info -> {db_res['info']}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
