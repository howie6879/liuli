#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：v1 接口函数
    Changelog: all notable changes to this file will be documented
"""
from flask import Blueprint, current_app, request

bp_api = Blueprint("v1", __name__, url_prefix="/v1")


@bp_api.route("/ping", methods=["GET"], strict_slashes=False)
def ping():
    """
    示例接口
    :return:
    """
    # 获取基本配置
    return "pong"
