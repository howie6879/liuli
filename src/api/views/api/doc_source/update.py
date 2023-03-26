"""
    Created by howie.hu at 2023-03-26.
    Description: 更新 doc_source
    Changelog: all notable changes to this file will be documented
"""

import time

from flask import current_app, request

from src.api.common import UniResponse, jwt_required, response_handle
from src.databases import MongodbBase, mongodb_update_data


@jwt_required()
def doc_source_update():
    """更新 doc_source
    eg:
    {
        "username": "liuli",
        "name": "wechat",
        "author": "liuli_team",
        "doc_source": "liuli_wechat",
        "collector": {
            "wechat": {
            "wechat_list": [
                "老胡的储物柜",
                "是不是很酷"
            ],
            "delta_time": 5,
            "spider_type": "sg_ruia",
            "spider_type_des": "当镜像是schedule:playwright_*时，spider_type可填写sg_playwright"
            }
        },
        "processor": {
            "before_collect": [],
            "after_collect": [
            {
                "func": "ad_marker",
                "cos_value": 0.6
            },
            {
                "func": "to_rss",
                "doc_source_list": [
                "liuli_wechat"
                ],
                "link_source": "github"
            }
            ]
        },
        "sender": {
            "sender_list": [
            "wecom"
            ],
            "query_days": 7,
            "delta_time": 3,
            "custom_filter": {
            "wecom": {
                "delta_time": 1,
                "ignore_doc_source_name": [
                ""
                ]
            }
            }
        },
        "backup": {
            "backup_list": [
            "github",
            "mongodb"
            ],
            "query_days": 7,
            "delta_time": 3,
            "init_config": {},
            "after_get_content": [
            {
                "func": "str_replace",
                "before_str": "data-src=\"",
                "after_str": "src=\"https://images.weserv.nl/?url="
            }
            ]
        },
        "schedule": {
            "period_list": [
            "00:10",
            "12:10",
            "21:10"
            ]
        }
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_doc_source")
    # 获取基础数据
    post_data: dict = request.json
    username = post_data.pop("username", "")
    doc_source = post_data.get("doc_source", "")

    db_res = mongodb_update_data(
        coll_conn=coll,
        filter_dict={"doc_source": doc_source, "username": username},
        update_data={
            "$set": {
                "username": username,
                "doc_source": doc_source,
                "data": post_data,
                "updated_at": int(time.time()),
            }
        },
    )
    result = UniResponse.SUCCESS
    if not db_res["status"]:
        # 更新失败
        result = UniResponse.DB_ERR
        err_info = (
            f"update doc_source config failed! DB response info -> {db_res['info']}"
        )
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
