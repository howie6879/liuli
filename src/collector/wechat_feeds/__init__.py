#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：获取公众号文章列表
      此脚本依赖项目: https://github.com/hellodword/wechat-feeds
      2021-12: 已弃用
    Changelog: all notable changes to this file will be documented
"""
from .wechat_doc_spider import WechatDocSpider, run_wechat_doc_spider
from .wechat_name_spider import WechatNameSpider, run_wechat_name_spider
from .wechat_utils import wechat2url
