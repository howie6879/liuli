#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：获取公众号文章列表
    Changelog: all notable changes to this file will be documented
"""

import asyncio
import time

import ujson
import xmltodict

from ruia import Response, Spider
from ruia_motor import RuiaMotorUpdate, init_spider

from src.config import Config
from src.utils import md5_encryption


class WechatDocSpider(Spider):
    """
    微信RSS文章爬虫
    """

    collection = "2c_articles"
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 2}

    async def parse(self, response: Response):
        """
        爬虫解析函数
        :param response:
        :type response: Response
        """
        xml_data = await response.text()
        json_data = ujson.loads(ujson.dumps(xmltodict.parse(xml_input=xml_data)))
        channel_data = json_data["rss"]["channel"]
        item_data = channel_data["item"]

        json_title = channel_data["title"]
        wechat_name = json_title.split("|")[0].strip()
        wechat_des = channel_data["description"]
        for each in item_data:
            pub_date = each["pubDate"]
            doc_name, doc_link = each.get("title", ""), each.get("link", "")
            doc_id = md5_encryption(f"{doc_name}_{doc_link}_{wechat_name}")
            s_time = time.strptime(pub_date, "%a, %d %b %Y %H:%M:%S +0800")
            each_data = {
                "doc_id": doc_id,
                "doc_name": doc_name,
                "doc_des": each.get("description", ""),
                "doc_link": doc_link,
                "doc_content": each.get("content:encoded", ""),
                "doc_date": time.strftime("%Y-%m-%d", s_time),
                "doc_ts": time.mktime(s_time),
                "doc_source": "wechat",
                "doc_source_name": wechat_name,
                "doc_source_des": wechat_des,
                "doc_ext": {},
            }
            yield RuiaMotorUpdate(
                collection=self.collection,
                filter={
                    "doc_name": each_data["doc_name"],
                    "doc_link": each_data["doc_link"],
                    "doc_source_name": each_data["doc_source_name"],
                },
                update={"$set": each_data},
                upsert=True,
            )

            # yield self.request(
            #     url=doc_link, metadata=each_data, callback=self.parse_url
            # )

    async def parse_url(self, response: Response):
        """
        解析链接内容
        :param response:
        :return:
        """
        each_data = response.metadata
        each_data["html"] = await response.text()
        yield RuiaMotorUpdate(
            collection=self.collection,
            filter={
                "doc_name": each_data["doc_name"],
                "doc_link": each_data["doc_link"],
                "doc_source_name": each_data["doc_source_name"],
            },
            update={"$set": each_data},
            upsert=True,
        )


async def init_motor_after_start(spider_ins):
    """
    初始化ruia-motor插件，数据自动持久化到MongoDB
    """
    spider_ins.mongodb_config = Config.MONGODB_CONFIG
    init_spider(spider_ins=spider_ins)


def run_wechat_doc_spider(start_urls: list = None, loop=None):
    """
    启动爬虫，这样写启动爬虫的目的是为了多次调度，如果自动关闭了事件循环就会出错
    :param start_urls:
    :param loop:
    :return:
    """
    loop = loop or asyncio.get_event_loop()
    WechatDocSpider.start_urls = start_urls
    WechatDocSpider.start(
        loop=loop, after_start=init_motor_after_start, close_event_loop=False
    )


if __name__ == "__main__":
    from src.collector.wechat import wechat2url

    wechat_urls = wechat2url(Config.WECHAT_LIST)
    run_wechat_doc_spider(list(wechat_urls.values()))
