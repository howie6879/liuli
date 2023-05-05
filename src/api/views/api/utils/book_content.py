"""
    Created by howie.hu at 2023-03-26.
    Description: 基于readability算法提取文章核心内容
    Changelog: all notable changes to this file will be documented
"""

from flask import request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import extract_core_html


@jwt_required()
def utils_book_content():
    """
    基于readability算法提取文章核心内容
    {
        "username": "liuli",
        "url": "https://www.yruan.com/article/38563/4082438.html"
    }
    """
    # 获取基础数据
    post_data: dict = request.json
    url = post_data.get("url") or ""
    result = UniResponse.SUCCESS
    core_html = ""
    if url:
        # 章节链接必须存在
        resp_text = get_html_by_requests(
            url, headers={"User-Agent": Config.LL_SPIDER_UA}
        )
        _, core_html = extract_core_html(resp_text)
        result = {
            ResponseField.DATA: {
                "url": url,
                "core_html": core_html,
            },
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.PARAM_ERR

    return response_handle(request=request, dict_value=result)
