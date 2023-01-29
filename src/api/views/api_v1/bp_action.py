"""
    Created by howie.hu at 2022-05-23.
    Description: 操作相关 API
    Changelog: all notable changes to this file will be documented
"""

import json

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
from src.backup.action import backup_doc
from src.config import Config
from src.databases import MongodbBase, mongodb_find_by_page
from src.processor.rss_utils import to_rss
from src.utils import LOGGER, get_ip, ts_to_str_date

bp_action = Blueprint("bp_action", __name__, url_prefix="/action")


@bp_action.route("/articles", methods=["POST"], strict_slashes=False)
@jwt_required()
def articles():
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
    app_logger: LOGGER = current_app.config["app_logger"]
    app_config: Config = current_app.config["app_config"]
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


@bp_action.route("/backup_generate", methods=["POST"], strict_slashes=False)
@jwt_required()
def backup_generate():
    """对数据源进行备份
    eg:
    {
        "username": "liuli",
        "basic_filter": {
            "doc_source": "liuli_wechat"
        },
        "backup_list": [
            "mongodb"
        ],
        "query_days": 7,
        "delta_time": 0,
        "init_config": {},
        "after_get_content": [
            {
            "func": "str_replace",
            "before_str": "data-src=\"",
            "after_str": "src=\"https://images.weserv.nl/?url="
            }
        ]
    }
    Returns:
        Response: 响应类
    """
    app_logger: LOGGER = current_app.config["app_logger"]
    # 获取基础数据
    post_data: dict = request.json
    del post_data["username"]
    result = UniResponse.SUCCESS
    try:
        backup_doc(post_data)
    except Exception as e:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.GEN_BACKUP_FAILED,
            ResponseField.STATUS: ResponseCode.GEN_BACKUP_FAILED,
        }
        err_info = f"gen backup failed! response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)


@bp_action.route("/rss_generate", methods=["POST"], strict_slashes=False)
@jwt_required()
def rss_generate():
    """生成目标 rss 源
    eg:
    {
        "username": "liuli",
        "doc_source_list": ["liuli_wechat"],
        "link_source": "mongodb",
        "rss_count": 20
    }
    Returns:
        Response: 响应类
    """
    app_logger: LOGGER = current_app.config["app_logger"]
    # 获取基础数据
    post_data: dict = request.json
    doc_source_list = post_data.get("doc_source_list", [])
    link_source = post_data.get("link_source", "")
    rss_count = int(post_data.get("rss_count", "20"))
    skip_ads = bool(post_data.get("skip_ads", "0") == "1")

    result = UniResponse.SUCCESS
    try:
        to_rss(
            doc_source_list=doc_source_list,
            link_source=link_source,
            skip_ads=skip_ads,
            rss_count=rss_count,
        )
    except Exception as e:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.GEN_RSS_FAILED,
            ResponseField.STATUS: ResponseCode.GEN_RSS_FAILED,
        }
        err_info = f"gen rss failed! response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)


@bp_action.route("/rss_list", methods=["POST"], strict_slashes=False)
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
