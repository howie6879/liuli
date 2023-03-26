"""
    Created by howie.hu at 2023-03-26.
    Description: 获取用户下所有 RSS 链接地址
    Changelog: all notable changes to this file will be documented
"""


from urllib.parse import urljoin

from flask import current_app, request

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
from src.utils import get_ip, ts_to_str_date


@jwt_required()
def action_rss_list():
    """获取用户下所有 RSS 链接地址
    eg:
    {
        "username": "liuli",
        "doc_source": "",
    }
    Returns:
        Response: 响应类
    """
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    app_config: Config = current_app.config["app_config"]
    coll = mongodb_base.get_collection(coll_name="liuli_rss")
    # 获取基础数据
    post_data: dict = request.json
    doc_source = post_data.get("doc_source", "")
    filter_dict = {"doc_source": doc_source} if doc_source else {}
    return_dict = {"_id": 0, "doc_source": 1, "doc_source_name": 1, "updated_at": 1}
    domain: str = app_config.LL_DOMAIN or f"http://{get_ip()}:{Config.LL_HTTP_PORT}"

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
