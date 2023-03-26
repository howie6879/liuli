"""
    Created by howie.hu at 2023-03-26.
    Description: 用户登录接口
    Changelog: all notable changes to this file will be documented
"""

from flask import request

from src.api.common import UniResponse, jwt_required, response_handle


@jwt_required()
def user_token_valid():
    """验证jwt是否有效
    eg:
    {
        "username": "liuli"
    }
    Returns:
        Response: 响应类
    """
    return response_handle(request=request, dict_value=UniResponse.SUCCESS)
