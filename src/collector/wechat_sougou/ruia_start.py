"""
    Created by howie.hu at 2022-01-13.
    Description: 基于Ruia爬虫框架的微信公众号爬虫
    Changelog: all notable changes to this file will be documented
"""
import re

from ruia import Response, Spider
from ruia_ua import middleware as ua_middleware

from src.collector.wechat_sougou.items import SGWechatItem, WechatItem


class SGWechatSpider(Spider):
    """微信文章爬虫"""

    name = "SGWechatSpider"
    request_config = {"RETRIES": 3, "DELAY": 5, "TIMEOUT": 20}
    concurrency = 10
    wechat_name = ""
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response: Response):
        """解析公众号原始链接数据"""
        html = await response.text()
        item_list = []
        async for item in SGWechatItem.get_items(html=html):
            if item.wechat_name == self.wechat_name:
                item_list.append(item)
                yield self.request(
                    url=item.latest_href,
                    metadata=item.results,
                    callback=self.parse_real_wechat_url,
                )
                break

    async def parse_real_wechat_url(self, response: Response):
        """解析公众号真实URL"""
        html = await response.text()
        real_wechat_url = ""
        target_str_list = re.findall(r"url \+\=\s\'(.+)';", html)
        for each in target_str_list:
            real_wechat_url += each.strip()
        real_wechat_url.replace("@", "")
        yield self.request(
            url=real_wechat_url,
            metadata=response.metadata,
            callback=self.parse_wechat,
        )

    async def parse_wechat(self, response: Response):
        """解析公众号元数据"""
        html = await response.text()
        wechat_item: WechatItem = await WechatItem.get_item(html=html)
        print(wechat_item)


if __name__ == "__main__":
    sg_url = "https://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&_sug_=n&_sug_type_="
    SGWechatSpider.wechat_name = "老胡的储物柜"
    SGWechatSpider.start_urls = [sg_url.format(SGWechatSpider.wechat_name)]
    SGWechatSpider.start(middleware=ua_middleware)
