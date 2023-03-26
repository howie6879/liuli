"""
    Created by howie.hu at 2023-03-26.
    Description: 生成 RSS
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
from src.processor.rss_utils import to_rss


@jwt_required()
def action_gen_rss():
    """生成目标 RSS 源
    eg:
    {
        "username": "liuli",
        "doc_source_list": ["liuli_wechat"],
        "link_source": "mongodb",
        "rss_count": 20
    }
    Returns:
        Response: 响应类
    """
    app_logger = current_app.config["app_logger"]
    # 获取基础数据
    post_data: dict = request.json
    doc_source_list = post_data.get("doc_source_list", [])
    link_source = post_data.get("link_source", "")
    rss_count = int(post_data.get("rss_count", "20"))
    skip_ads = bool(post_data.get("skip_ads", "0") == "1")

    result = UniResponse.SUCCESS
    try:
        to_rss(
            doc_source_list=doc_source_list,
            link_source=link_source,
            skip_ads=skip_ads,
            rss_count=rss_count,
        )
    except Exception as e:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.GEN_RSS_FAILED,
            ResponseField.STATUS: ResponseCode.GEN_RSS_FAILED,
        }
        err_info = f"gen rss failed! response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
