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

from src.collector.wechat.wechat_utils import get_wf_url
from src.config import Config


class WechatNameSpider(Spider):
    """
    微信公众号名称爬虫
    """

    collection = "2c_wechat_name"
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 5}
    aiohttp_kwargs = {"proxy": Config.PROXY} if Config.PROXY else {}

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


def run_wechat_name_spider(loop=None):
    """
    启动爬虫，这样写启动爬虫的目的是为了多次调度，如果自动关闭了事件循环就会出错
    :param loop: 事件循环
    :return:
    """
    loop = loop or asyncio.get_event_loop()
    start_urls = [loop.run_until_complete(get_wf_url())]

    WechatNameSpider.start_urls = start_urls
    spider = WechatNameSpider.start(
        loop=loop, after_start=init_motor_after_start, close_event_loop=False
    )
    return spider


if __name__ == "__main__":
    run_wechat_name_spider()
