#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：
    Changelog: all notable changes to this file will be documented
"""
from flask import Blueprint, current_app, request

from src.databases import MongodbBase

bp_api = Blueprint(__name__, __name__, url_prefix="/v1")


@bp_api.route("/2c/", methods=["POST"], strict_slashes=False)
def predict():
    """
    是否广告预测接口
    :return:
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    post_data = request.json
    date = post_data.get("date")
