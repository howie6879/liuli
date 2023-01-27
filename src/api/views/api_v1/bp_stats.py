"""
    Created by howie.hu at 2022-05-23.
    Description: 统计相关 API
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

bp_stats = Blueprint("stats", __name__, url_prefix="/stats")


@bp_stats.route("/source_list", methods=["POST"], strict_slashes=False)
@jwt_required()
def source_list():
    """获取所有文档源统计信息
    eg:
    {
        "username": "liuli"
    }
    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger: LOGGER = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_articles")
    try:
        doc_source_list = coll.distinct("doc_source")
        doc_source_dict = {
            "doc_source_list": [],
            "doc_source_name_list": doc_source_list,
            "doc_source_counts": len(doc_source_list),
            "doc_counts": 0,
        }
        for doc_source in doc_source_list:
            pipeline = [
                {"$match": {"doc_source": doc_source}},
                {"$group": {"_id": "$doc_source_name", "count": {"$sum": 1}}},
            ]
            each_doc_source: dict = {
                "counts": 0,
                "rows": [],
                "rows_info": [],
            }

            for item in coll.aggregate(pipeline):
                each_doc_source["rows"].append(item["_id"])
                each_doc_source["rows_info"].append(item)
                each_doc_source["counts"] += item["count"]
                doc_source_dict["doc_counts"] += item["count"]
            doc_source_dict["doc_source_list"].append({doc_source: each_doc_source})

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
