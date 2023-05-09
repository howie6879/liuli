"""
    Created by howie.hu at 2023-05-05.
    Description: 文档模糊搜索接口
    Changelog: all notable changes to this file will be documented
"""

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
from src.utils.tools import text_decompress


@jwt_required()
def articles_fuzzy_search():
    """
    文档模糊搜索接口
    """
    pass
