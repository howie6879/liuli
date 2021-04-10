#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：获取公众号rss文件，然后获取公众号最近推文入库作为样本
        此脚本依赖项目：https://github.com/hellodword/wechat-feeds
    Changelog: all notable changes to this file will be documented
"""
import asyncio

import aiohttp
import ujson

from ruia import Request

from src.collector.wechat.utils import get_wf_url
from src.collector.wechat.wechat_doc_spider import (
    WechatDocSpider,
    init_motor_after_start,
)

_RSS_TEM = "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/{0}.xml"


async def get_wf_docs():
    """
    抓取RSS下最近所有文章
    :return:
    """
    url = await get_wf_url()
    start_urls = []
    async with aiohttp.ClientSession() as session:
        resp = await Request(url=url, request_session=session).fetch()
        json_data = ujson.loads(await resp.text())
        for each in json_data:
            bizid = each["bizid"]
            cur_rss_url = _RSS_TEM.format(bizid)
            start_urls.append(cur_rss_url)
    # 偶尔有些公众号字段由于原项目兼容问题会出错
    # 但是作为训练集，少几条无所谓，如果正式获取出现错误再针对性地解决
    WechatDocSpider.start_urls = start_urls
    WechatDocSpider.collection = "2c_wechat_datasets"
    await WechatDocSpider.async_start(after_start=init_motor_after_start)
    print(f"共更新 {len(json_data)} 个公众号")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(get_wf_docs())
