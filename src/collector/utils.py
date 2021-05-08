#!/usr/bin/env python
"""
    Created by howie.hu at 2021/04/29.
    Description: 采集器相关通用工具函数
    Changelog: all notable changes to this file will be documented
"""

import html2text
import requests

from readability import Document
from textrank4zh import TextRank4Keyword

from src.utils import LOGGER


def fetch_keyword_list(url_or_text: str = None):
    """
    获取文本的关键词列表
    :param url_or_text:
    :return:
    """
    if url_or_text.startswith("http"):
        resp = send_get_request(url_or_text)
        text = html_to_text(resp.text)
    else:
        text = url_or_text
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2, vertex_source="words_no_stop_words")
    keyword_list = []
    for item in tr4w.get_keywords(20, word_min_len=2):
        keyword_list.append(item.word)

    return keyword_list


def html_to_text(html: str):
    """
    从html提取核心内容text
    :param html:
    :return:
    """
    doc = Document(html)
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = False
    h.unicode_snob = False
    text = h.handle(doc.summary())
    return text.strip()


def send_get_request(url, params: dict = None, **kwargs):
    """
    发起GET请求
    :param url: 请求目标地址
    :param params: 请求参数
    :param kwargs:
    :return:
    """
    try:
        resp = requests.get(url, params, **kwargs)
    except Exception as e:
        resp = None
        LOGGER.exception(f"请求出错 - {url} - {str(e)}")
    return resp


if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/RWO0xF6zKBJ6y_ClYaDLXg"

    resp = requests.get(url)
    text = html_to_text(resp.text)
    res = fetch_keyword_list(url)
    print(res)
