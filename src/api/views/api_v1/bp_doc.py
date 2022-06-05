"""
    Created by howie.hu at 2022-05-23.
    Description: 文章相关API
    Changelog: all notable changes to this file will be documented
"""

from urllib.parse import urljoin

from flask import Blueprint, current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.config import Config
from src.databases import MongodbBase
from src.utils import LOGGER, get_ip, ts_to_str_date

bp_doc = Blueprint("doc", __name__, url_prefix="/doc")


@bp_doc.route("/articles", methods=["POST"], strict_slashes=False)
@jwt_required()
def articles():
    """查询历史文章
    {
        "username": "liuli",
        "doc_source": "",
        "doc_source_name": ""
    }

    Returns:
        Response: 响应类
    """


@bp_doc.route("/rss_list", methods=["POST"], strict_slashes=False)
@jwt_required()
def rss_list():
    """获取用户下所有rss链接地址
    eg:
    {
        "username": "liuli",
        "doc_source": "",
    }
    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger: LOGGER = current_app.config["app_logger"]
    app_config: Config = current_app.config["app_config"]
    coll = mongodb_base.get_collection(coll_name="liuli_rss")
    # 获取基础数据
    post_data: dict = request.json
    doc_source = post_data.get("doc_source", "")
    filter_dict = {"doc_source": doc_source} if doc_source else {}
    return_dict = {"_id": 0, "doc_source": 1, "doc_source_name": 1, "updated_at": 1}
    domain: str = app_config.DOMAIN or f"http://{get_ip()}:{Config.HTTP_PORT}"

    try:
        cursor = coll.find(filter_dict, return_dict).sort("updated_at", 1)
        rss_dict = []
        for document in cursor:
            updated_at = document["updated_at"]
            doc_source = document["doc_source"]
            doc_source_name = document["doc_source_name"]
            rss_dict.append(
                {
                    **document,
                    **{
                        "updated_at": ts_to_str_date(updated_at),
                        "rss_url": urljoin(
                            domain, f"rss/{doc_source}/{doc_source_name}"
                        ),
                    },
                }
            )
        result = {
            ResponseField.DATA: rss_dict,
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    except Exception as e:
        result = UniResponse.DB_ERR
        err_info = f"query doc RSS failed! DB response info -> {e}"
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)


@bp_doc.route("/source_list", methods=["POST"], strict_slashes=False)
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
