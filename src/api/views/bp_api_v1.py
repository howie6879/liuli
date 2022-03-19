#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：v1 接口函数
    Changelog: all notable changes to this file will be documented
"""
from flask import Blueprint, request

from src.api.common import ResponseField, UniResponse, response_handle
from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import extract_chapters, extract_core_html

bp_api = Blueprint("v1", __name__, url_prefix="/v1")


@bp_api.route("/ping", methods=["GET"], strict_slashes=False)
def ping():
    """
    示例接口: http://127.0.0.1:8765/v1/ping
    :return:
    """
    # 获取基本配置
    return "pong"


@bp_api.route("/book_chapter", methods=["GET"], strict_slashes=False)
def book_chapter():
    """
    返回书籍目录json，依赖参数：
        - url: 书籍目录链接
    eg: http://0.0.0.0:8765/v1/book_chapter?url=https://www.yruan.com/article/38563.html
    """
    args = request.args.to_dict()
    url = args.get("url", "")
    chapter_list = []
    result = UniResponse.SUCCESS
    if url:
        # 目录链接必须存在
        resp_text = get_html_by_requests(url, headers={"User-Agent": Config.SPIDER_UA})
        chapter_list = extract_chapters(url, resp_text)
    else:
        result = UniResponse.PARAM_ERR

    result[ResponseField.DATA] = {
        "url": url,
        "chapter_list": chapter_list,
    }
    return response_handle(request=request, dict_value=result)


@bp_api.route("/book_content", methods=["GET"], strict_slashes=False)
def book_content():
    """
    基于readability算法提取文章核心内容，并转化为MD格式输出
    返回书籍目录json，依赖参数：
        - url: 书籍章节页链接
    eg: http://0.0.0.0:8765/v1/book_content?url=https://www.yruan.com/article/38563/4082438.html
    """
    args = request.args.to_dict()
    url = args.get("url", "")
    result = UniResponse.SUCCESS
    core_html = ""
    if url:
        # 章节链接必须存在
        resp_text = get_html_by_requests(url, headers={"User-Agent": Config.SPIDER_UA})
        _, core_html = extract_core_html(resp_text)
    else:
        result = UniResponse.PARAM_ERR

    result[ResponseField.DATA] = {
        "url": url,
        "core_html": core_html,
    }
    return response_handle(request=request, dict_value=result)
