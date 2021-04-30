#!/usr/bin/env python
"""
    Created by howie.hu at 2021/04/29.
    Description: 采集器相关通用工具函数
    Changelog: all notable changes to this file will be documented
"""

from newspaper import Article
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def fetch_keyword_list(url: str):
    """
    获取文章简要说明作为样本
    失败就会出现 ['该内容已被发布者删除']
    :param url:
    :return:
    """
    article = Article(url, language="zh")
    article.download()
    article.parse()
    tr4w = TextRank4Keyword()
    tr4w.analyze(
        text=article.text, lower=True, window=2, vertex_source="words_no_stop_words"
    )
    keyword_list = []
    for item in tr4w.get_keywords(20, word_min_len=2):
        keyword_list.append(item.word)

    return keyword_list
