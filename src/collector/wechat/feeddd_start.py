"""
    Created by leeorz.
    Description：
    采集器：
        - 基于 src/collector/wechat_sougou/items/wechat_item.py的公众号采集
        - 基于 feedparser,从feeddd解析rss
    Changelog: all notable changes to this file will be documented
"""
import asyncio

import feedparser

from ruia import Response, Spider
from ruia_ua import middleware as ua_middleware

from src.collector.utils import load_data_to_articlles
from src.collector.wechat.items import WechatItem
from src.processor import html_to_text_h2t
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption


class WeiXinSpider(Spider):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """

    name = "WeiXinSpider"
    request_config = {"RETRIES": 3, "DELAY": 3, "TIMEOUT": 5}
    concurrency = 10
    wechat_name = ""
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response: Response):
        """解析公众号元数据"""
        html = await response.text()
        wechat_item: WechatItem = await WechatItem.get_item(html=html)
        wechat_data = {
            **wechat_item.results,
            **{
                "doc_id": md5_encryption(f"{wechat_item.doc_name}_{self.wechat_name}"),
                "doc_keywords": "",
                "doc_source_name": self.wechat_name,
                "doc_link": response.url,
                "doc_source": "liuli_wechat",
                "doc_source_account_nick": wechat_item.doc_source_account_nick,
                "doc_source_account_intro": wechat_item.doc_source_account_intro,
                "doc_content": html_to_text_h2t(html),
                "doc_html": "",
            },
        }
        await asyncio.coroutine(load_data_to_articlles)(input_data=wechat_data)


def run(collect_config: dict):
    """rss解析，并使用WeiXinSpider抓取rss条目，并持久化

    Args:
        collect_config (dict, optional): 采集器配置
    """
    feeds_dict: dict = collect_config.get("feeds_dict")
    feeds_name: list = list(feeds_dict)
    delta_time = collect_config.get("delta_time", 3)
    WeiXinSpider.request_config = {
        "RETRIES": 3,
        "DELAY": delta_time,
        "TIMEOUT": 5,
    }
    for name in feeds_name:
        WeiXinSpider.wechat_name = name
        LOGGER.info(f"rss源 {name}: {feeds_dict[name]}")
        fd = feedparser.parse(feeds_dict[name])
        urls = []
        for entry in fd.entries:
            LOGGER.info(entry.link)
            urls.append(entry.link)
        WeiXinSpider.start_urls = urls
        WeiXinSpider.start(middleware=ua_middleware)
