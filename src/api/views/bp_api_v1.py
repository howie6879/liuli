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
from src.processor.text_utils import extract_chapters

bp_api = Blueprint("v1", __name__, url_prefix="/v1")


@bp_api.route("/ping", methods=["GET"], strict_slashes=False)
def ping():
    """
    示例接口
    :return:
    """
    # 获取基本配置
    return "pong"


@bp_api.route("/book", methods=["GET"], strict_slashes=False)
def book():
    """
    返回书籍目录json，依赖参数：
        - url: 书籍目录链接
        - resp_type: html or json
    """
    args = request.args.to_dict()
    resp_type = args.get("resp_type", "json")
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
        "resp_type": resp_type,
        "chapter_list": chapter_list,
    }
    return response_handle(request=request, dict_value=result)
