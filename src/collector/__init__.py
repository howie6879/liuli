#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：
    采集器：基于 Ruia 爬虫框架编写（pip install ruia）：https://github.com/howie6879/ruia
        - 公众号
        - RSS
        - 博客
    Changelog: all notable changes to this file will be documented
"""
from .utils import fetch_keyword_list, html_to_text_h2t, send_get_request
from .wechat_sougou import run_wechat_doc_spider
