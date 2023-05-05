"""
    Created by howie.hu at 2022-02-09.
    Description: 文档元数据相关通用函数
    Changelog: all notable changes to this file will be documented
"""
from urllib.parse import quote

from src.config import Config
from src.utils import get_ip


def get_bak_doc_link(link_source: str, doc_data: dict) -> str:
    """返回不同存储器下的 href

    Args:
        link_source (str): 链接返回规则类型
        doc_data (dict): 文章数据
    """
    doc_source = doc_data["doc_source"]
    doc_source_name = doc_data["doc_source_name"]
    doc_name = quote(doc_data["doc_name"])

    if link_source == "github":
        github_domain = Config.LL_GITHUB_DOMAIN
        doc_link = f"{github_domain}/{doc_source}/{doc_source_name}/{doc_name}.html"
    elif link_source == "mongodb":
        domain: str = Config.LL_DOMAIN or f"{get_ip()}:{Config.LL_HTTP_PORT}"
        doc_link = f"{domain}/backup/{doc_source}/{doc_source_name}/{doc_name}"
    else:
        doc_link = doc_data["doc_link"]

    return doc_link
