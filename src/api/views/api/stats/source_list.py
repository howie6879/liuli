"""
    Created by howie.hu at 2023-03-26.
    Description: 获取所有文档源统计信息
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
from src.databases import MongodbBase, mongodb_find


@jwt_required()
def stats_source_list():
    """获取所有文档源统计信息
    eg:
    {
        "username": "liuli"
    }
    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    article_coll = mongodb_base.get_collection(coll_name="liuli_articles")
    doc_source_coll = mongodb_base.get_collection(coll_name="liuli_doc_source")

    try:
        doc_source_res = mongodb_find(doc_source_coll, {}, {"_id": 0})

        if doc_source_res["status"]:
            p_doc_source_dict = {}
            for each in doc_source_res["info"]:
                p_doc_source_dict[each["doc_source"]] = {
                    "doc_source_alias_name": each["doc_source_alias_name"]
                }

            all_doc_source_dict = {
                "doc_source_stats_dict": {},
                "doc_source_counts": len(p_doc_source_dict),
                "doc_counts": 0,
            }

            for doc_source, doc_source_data in p_doc_source_dict.items():
                pipeline = [
                    {"$match": {"doc_source": doc_source}},
                    {
                        "$group": {
                            "_id": "$doc_source_name",
                            "doc_source_account_intro": {
                                "$last": "$doc_source_account_intro"
                            },
                            # "doc_source_alias_name": {"$last": "$doc_source_alias_name"},
                            "doc_source_account_nick": {
                                "$last": "$doc_source_account_nick"
                            },
                            "count": {"$sum": 1},
                        }
                    },
                ]
                each_doc_source: dict = {
                    "counts": 0,
                    "rows": [],
                    "rows_info": [],
                    "doc_source_alias_name": doc_source_data["doc_source_alias_name"],
                }

                for item in article_coll.aggregate(pipeline):
                    # 外部字典数据处理
                    all_doc_source_dict["doc_counts"] += item["count"]
                    # 内部字典数据处理
                    each_doc_source["rows"].append(item["_id"])
                    each_doc_source["rows_info"].append(item)
                    each_doc_source["counts"] += item["count"]

                all_doc_source_dict["doc_source_stats_dict"].update(
                    {doc_source: each_doc_source}
                )

            result = {
                ResponseField.DATA: all_doc_source_dict,
                ResponseField.MESSAGE: ResponseReply.SUCCESS,
                ResponseField.STATUS: ResponseCode.SUCCESS,
            }

        else:
            result = UniResponse.DB_ERR
            err_info = f"query liuli_doc_source failed! DB response info -> {doc_source_res['info']}"
            app_logger.error(err_info)

    except Exception as e:
        result = UniResponse.DB_ERR
        err_info = f"query doc source failed! DB response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
