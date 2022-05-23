"""
    Created by howie.hu at 2022-05-23.
    Description: 文章相关API
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint, current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase
from src.utils import LOGGER

bp_doc = Blueprint("doc", __name__, url_prefix="/doc")


@bp_doc.route("/doc_source_list", methods=["POST"], strict_slashes=False)
@jwt_required()
def token_valid():
    """获取所有文档源统计信息
    eg:
    {
        "username": "liuli"
    }
    doc_source 为空表示查询所有源信息
    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger: LOGGER = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_articles")
    try:
        doc_source_list = coll.distinct("doc_source")
        doc_source_dict = {}
        for doc_source in doc_source_list:
            pipeline = [
                {"$match": {"doc_source": doc_source}},
                {"$group": {"_id": "$doc_source_name", "count": {"$sum": 1}}},
            ]
            doc_source_dict[doc_source] = {
                "doc_count": 0,
                "doc_source_list": [],
                "doc_source_details": [],
            }
            for item in coll.aggregate(pipeline):
                doc_source_list: list = doc_source_dict[doc_source]["doc_source_list"]
                doc_source_list.append(item["_id"])
                doc_source_details: list = doc_source_dict[doc_source][
                    "doc_source_details"
                ]
                doc_source_details.append(item)
                doc_source_dict[doc_source]["doc_count"] += item["count"]
        result = {
            ResponseField.DATA: doc_source_dict,
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    except Exception as e:
        result = UniResponse.DB_ERR
        err_info = f"query doc source failed! DB response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
