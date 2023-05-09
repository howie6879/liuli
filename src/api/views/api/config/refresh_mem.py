"""
    Created by howie.hu at 2023-05-09.
    Description: 刷新当前内存配置
    Changelog: all notable changes to this file will be documented
"""

import json

from bson import json_util
from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_find


@jwt_required()
def config_refresh_mem():
    """
    刷新当前内存配置
    eg:
    {
        "username": "liuli"
    }
    """
