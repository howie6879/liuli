"""
    Created by howie.hu at 2023-03-26.
    Description: 检察服务可用性
    Changelog: all notable changes to this file will be documented
"""
import json
import os

from flask import current_app

from src.config import Config


def ping():
    """
    v1 描述接口: http://127.0.0.1:8765/v1/
    :return:
    """
    app_config: Config = current_app.config["app_config"]
    api_json_path = os.path.join(app_config.API_DIR, "views/api/api.json")
    with open(api_json_path, "r", encoding="utf-8") as f:
        resp = json.load(f)
    return resp
