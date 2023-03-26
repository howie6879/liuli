#!/usr/bin/env python
"""
    Created by howie.hu at 2022/4/12.
    Description：
    Changelog: all notable changes to this file will be documented
"""
import json
import os

from flask import Blueprint, current_app

from src.config import Config

from .bp_action import bp_action
from .bp_doc_source import bp_doc_source
from .bp_stats import bp_stats
from .bp_user import bp_user
from .bp_utils import bp_utils

bp_api_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")

bp_api_v1.register_blueprint(bp_action)
bp_api_v1.register_blueprint(bp_doc_source)
bp_api_v1.register_blueprint(bp_stats)
bp_api_v1.register_blueprint(bp_user)
bp_api_v1.register_blueprint(bp_utils)


@bp_api_v1.route("/", methods=["GET"], strict_slashes=False)
def ping():
    """
    v1 描述接口: http://127.0.0.1:8765/v1/
    :return:
    """
    app_config: Config = current_app.config["app_config"]
    api_json_path = os.path.join(app_config.API_DIR, "views/api_v1/api.json")
    with open(api_json_path, "r", encoding="utf-8") as f:
        resp = json.load(f)
    return resp
