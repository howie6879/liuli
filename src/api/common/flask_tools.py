"""
    Created by howie.hu at 2022-02-11.
    Description: Flask 一些常用功能封装
    Changelog: all notable changes to this file will be documented
"""

import json

from flask import jsonify
from werkzeug.local import LocalProxy


def response_handle(*, request: LocalProxy, dict_value: dict, status: int = 200):
    """
    构造一个json格式的响应
    Args:
        request (LocalProxy): flask request实例
        dict_value (dict): 数据字典
        status (int, optional): 状态码. Defaults to 200.
    """
    if isinstance(request, LocalProxy):
        resp = jsonify(dict_value), status
    else:
        resp = json.dumps(dict_value, ensure_ascii=False)
    return resp
