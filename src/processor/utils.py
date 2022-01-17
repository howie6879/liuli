"""
    Created by howie.hu at 2021-12-30.
    Description: 通用处理函数
    Changelog: all notable changes to this file will be documented
"""

import os

import html2text

from readability import Document
from textrank4zh import TextRank4Keyword

from src.common.remote import send_get_request
from src.config import Config


def str_replace(text: str, before_str: str, after_str: str):
    """文本替换

    Args:
        text (str): 原始文本
        before_str (str): 替换前
        after_str (str): 替换后
    """
    return str(text).replace(before_str, after_str)


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
    stop_file_path = os.path.join(
        os.path.join(Config.MODEL_DIR, "data"), "stop_words.txt"
    )
    tr4w = TextRank4Keyword(stop_words_file=stop_file_path)
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


if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw"
    resp = send_get_request(url)
    text = html_to_text_h2t(resp.text)
    print(text)
    res = fetch_keyword_list(url)
    print(res)
