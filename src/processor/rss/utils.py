"""
    Created by howie.hu at 2022-01-25.
    Description: RSS 生成相关处理函数
    Changelog: all notable changes to this file will be documented
"""

from src.config import Config
from src.utils import get_ip


def get_rss_doc_link(link_source: str, doc_data: dict):
    """返回 RSS 展示的 href

    Args:
        link_source (str): 链接返回规则类型
        doc_data (dict): 文章数据
    """
    doc_source = doc_data["doc_source"]
    doc_source_name = doc_data["doc_source_name"]
    doc_name = doc_data["doc_name"]

    if link_source == "github":
        github_domain = Config.GITHUB_DOMAIN
        doc_link = f"{github_domain}/{doc_source}/{doc_source_name}/{doc_name}.html"
    elif link_source == "mongodb":
        domain = Config.DOMAIN or f"{get_ip()}:{Config.HTTP_PORT}"
        doc_link = f"{domain}/backup/{doc_source}/{doc_source_name}/{doc_name}"
    else:
        doc_link = doc_data["doc_link"]

    return doc_link
