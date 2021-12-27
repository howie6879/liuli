#!/usr/bin/env python
"""
    Created by howie.hu at 2021/04/29.
    Description: wechat feeds 采集器相关通用工具函数
    Changelog: all notable changes to this file will be documented
"""

import os

import html2text
import requests

# from gne import GeneralNewsExtractor
from readability import Document
from textrank4zh import TextRank4Keyword

from src.config import Config
from src.utils import LOGGER


def fetch_keyword_list(url_or_text: str = None):
    """
    获取文本的关键词列表
    :param url_or_text:
    :return:
    """
    if url_or_text.startswith("http"):
        resp = send_get_request(url_or_text)
        # TODO 当text为空时候需要进行处理
        text = html_to_text_h2t(resp.text) if resp else None
    else:
        text = url_or_text
    tr4w = TextRank4Keyword(
        stop_words_file=os.path.join(Config.BASE_DIR, "model_data/data/stop_words.txt")
    )
    tr4w.analyze(text=text, lower=True, window=2)
    keyword_list = []
    for item in tr4w.get_keywords(20, word_min_len=2):
        keyword_list.append(item.word)

    return keyword_list


def html_to_text_h2t(html: str):
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


# def html_to_text_gne(html: str):
#     """
#     从html提取核心内容text
#     :param html:
#     :return:
#     """
#     extractor = GeneralNewsExtractor()
#     result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
#     return result.get("content").strip()

if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/GLo6hs2infzxynN64MjyIQ"
    resp = requests.get(url)
    text = html_to_text_h2t(resp.text)
    print(text)
    res = fetch_keyword_list(url)
    print(res)
