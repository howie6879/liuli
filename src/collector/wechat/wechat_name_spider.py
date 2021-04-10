#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：获取wechat-feeds支持的微信公众号名称，可根据原项目更新时间自动更新
    Changelog: all notable changes to this file will be documented
"""
import asyncio

import ujson

from ruia import Response, Spider
from ruia_motor import RuiaMotorUpdate, init_spider

from src.collector.wechat.utils import get_wf_url
from src.config import Config


class WechatNameSpider(Spider):
    """
    微信公众号名称爬虫
    """

    collection = "2c_wechat_name"
    start_urls = [asyncio.get_event_loop().run_until_complete(get_wf_url())]

    async def parse(self, response: Response):
        """
        爬虫解析函数
        :param response:
        :type response: Response
        """
        json_data = ujson.loads(await response.text())
        for each in json_data:
            yield RuiaMotorUpdate(
                collection=self.collection,
                filter={"name": each.get("name", "")},
                update={"$set": each},
                upsert=True,
            )


async def init_motor_after_start(spider_ins: Spider):
    """
    初始化ruia-motor插件，数据自动持久化到MongoDB
    """
    spider_ins.mongodb_config = Config.MONGODB_CONFIG
    init_spider(spider_ins=spider_ins)


if __name__ == "__main__":
    WechatNameSpider.start(after_start=init_motor_after_start)
