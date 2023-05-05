"""
    Created by howie.hu at 2023-03-26.
    Description: 返回书籍目录 json
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
from src.processor.text_utils import extract_chapters


@jwt_required()
def utils_book_chapter():
    """
    返回书籍目录 json
    {
        "username": "liuli",
        "url": "https://www.yruan.com/article/38563.html"
    }
    """
    # 获取基础数据
    post_data: dict = request.json
    url = post_data.get("url") or ""
    chapter_list = []
    result = UniResponse.SUCCESS
    if url:
        # 目录链接必须存在
        resp_text = get_html_by_requests(
            url, headers={"User-Agent": Config.LL_SPIDER_UA}
        )
        chapter_list = extract_chapters(url, resp_text)
        result = {
            ResponseField.DATA: {
                "url": url,
                "chapter_list": chapter_list,
            },
            ResponseField.MESSAGE: ResponseReply.SUCCESS,
            ResponseField.STATUS: ResponseCode.SUCCESS,
        }
    else:
        result = UniResponse.PARAM_ERR

    return response_handle(request=request, dict_value=result)
