#!/usr/bin/env python
"""
    Created by howie.hu at 2022/4/12.
    Description：
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint

from .bp_doc import bp_doc
from .bp_user import bp_user
from .bp_utils import bp_utils

bp_api_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")
bp_api_v1.register_blueprint(bp_user)
bp_api_v1.register_blueprint(bp_utils)
bp_api_v1.register_blueprint(bp_doc)


@bp_api_v1.route("/", methods=["GET"], strict_slashes=False)
def ping():
    """
    v1 描述接口: http://127.0.0.1:8765/v1/
    :return:
    """
    return {
        "version": "v1.0",
        "github": "https://github.com/liuli-io/liuli",
        "website": "https://liuli.io/",
        "api": {
            "/user": [
                {
                    "path": "v1/user/login",
                    "method": "post",
                    "description": "用户登录接口",
                    "request": {},
                    "response": {
                        "data": {"token": "..", "username": "liuli"},
                        "info": "ok",
                        "status": 200,
                    },
                },
                {
                    "path": "v1/user/token_valid",
                    "method": "post",
                    "description": "用户token校验接口",
                    "request": {"username": "liuli"},
                    "response": {"data": {}, "info": "ok", "status": 200},
                },
                {
                    "path": "v1/user/change_pwd",
                    "method": "post",
                    "description": "修改密码",
                    "request": {
                        "username": "liuli",
                        "o_password": "liuli",
                        "n_password": "liuli",
                    },
                    "response": {
                        "data": {"username": "liuli"},
                        "info": "ok",
                        "status": 200,
                    },
                },
            ],
            "/doc": [
                {
                    "path": "v1/doc/articles",
                    "method": "post",
                    "description": "查询历史文章",
                    "request": {
                        "username": "liuli",
                        "doc_source": "liuli_wechat",
                        "doc_source_name": "老胡的储物柜",
                        "size": 1,
                        "page": 1,
                    },
                    "response": {
                        "data": {
                            "counts": 21,
                            "detail_list": [
                                {
                                    "_id": {"$oid": "6227505ee43a4af747b70fda"},
                                    "doc_name": "我的周刊（第028期）",
                                    "doc_source": "liuli_wechat",
                                    "doc_source_name": "老胡的储物柜",
                                    "doc_ts": 1645795680.0,
                                }
                            ],
                            "page": 1,
                            "size": 1,
                        },
                        "info": "ok",
                        "status": 200,
                    },
                },
                {
                    "path": "v1/doc/rss_list",
                    "method": "post",
                    "description": "获取用户下所有rss链接地址",
                    "request": {"username": "liuli", "doc_source": "liuli_wechat"},
                    "response": {
                        "data": [
                            {
                                "doc_source": "liuli_wechat",
                                "doc_source_name": "老胡的储物柜",
                                "rss_url": "http://0.0.0.0:8765/rss/liuli_wechat/老胡的储物柜",
                                "updated_at": "2022-06-29 11:30:02",
                            }
                        ],
                        "info": "ok",
                        "status": 200,
                    },
                },
                {
                    "path": "v1/doc/source_list",
                    "method": "post",
                    "description": "获取所有文档源统计信息",
                    "request": {"username": "liuli"},
                    "response": {
                        "data": {
                            "liuli_wechat": {
                                "doc_count": 14,
                                "doc_source_details": [{"_id": "老胡的储物柜", "count": 14}],
                                "doc_source_list": ["老胡的储物柜"],
                            }
                        },
                        "info": "ok",
                        "status": 200,
                    },
                },
            ],
        },
    }
