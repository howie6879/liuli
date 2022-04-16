#!/usr/bin/env python
"""
    Created by howie.hu at 2022/4/12.
    Description：
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint

from .bp_user import bp_user
from .bp_utils import bp_utils

bp_api_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")
bp_api_v1.register_blueprint(bp_user)
bp_api_v1.register_blueprint(bp_utils)


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
        "description": {
            "/user": [
                {"path": "v1/user/login", "method": "post", "info": "用户登录接口"},
                {
                    "path": "v1/user/token_valid",
                    "method": "post",
                    "info": "用户token校验接口",
                },
            ]
        },
    }
