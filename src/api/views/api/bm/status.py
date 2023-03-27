"""
    Created by howie.hu at 2023-03-27.
    Description: 检查接口状态
    Changelog: all notable changes to this file will be documented
"""

from flask import request

from src.api.common import UniResponse, jwt_required, response_handle


@jwt_required()
def bm_status():
    """
    接口检测
    :return:
    """
    return response_handle(request=request, dict_value=UniResponse.SUCCESS)
