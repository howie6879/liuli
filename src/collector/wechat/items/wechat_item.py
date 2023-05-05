"""
    Created by howie.hu at 2021-12-22.
    Description: 基于 Ruia 的微信页面 Item 提取类
    Changelog: all notable changes to this file will be documented
"""

import time

from ruia import AttrField, HtmlField, Item, RegexField, Spider, TextField
from ruia_ua import middleware as ua_middleware

from src.utils.tools import text_compress, ts_to_str_date


class WechatItem(Item):
    """
    基于 Ruia 的微信页面 Item 提取类
    示例：https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw
    """

    # 文章标题
    # doc_name = AttrField(css_select='meta[property="og:title"]', attr="content")
    doc_name = AttrField(
        css_select='meta[property="og:title"]', attr="content", default=""
    )
    # 描述
    doc_des = AttrField(
        css_select='meta[property="og:description"]', attr="content", default=""
    )
    # 文章作者
    doc_author = AttrField(
        css_select='meta[property="og:article:author"]', attr="content", default=""
    )
    # 文章链接，这里的链接有过期时间，但是在微信体系内打开并不会过期，所以可以用
    doc_link = AttrField(
        css_select='meta[property="og:url"]', attr="content", default=""
    )
    # 文章发布时间戳
    doc_ts = RegexField(
        re_select=r"var ct = \"(\d{1,10})\"\;",
        default=time.time(),
    )
    # 文章发布日期
    doc_date = RegexField(
        re_select=r"var ct = \"(\d{1,10})\"\;",
        default=ts_to_str_date(time.time()),
    )
    # doc_date_f1 = TextField(css_select="em#publish_time", default="")
    # doc_date_f2 = RegexField(
    #     re_select=r"o=\"(20\d.*)\"\;",
    #     default=ts_to_str_date(time.time(), "%Y-%m-%d %H:%M"),
    # )
    # doc_ts_f1 = TextField(css_select="em#publish_time", default="")
    # doc_ts_f2 = RegexField(
    #     re_select=r"o=\"(20\d.*)\"\;",
    #     default=ts_to_str_date(time.time(), "%Y-%m-%d %H:%M"),
    # )
    # 文章图
    doc_image = AttrField(
        css_select='meta[property="og:image"]', attr="content", default=""
    )
    # 公众号名称
    doc_source_name = TextField(
        css_select="div.profile_inner>strong.profile_nickname", default=""
    )
    # 公众号元数据
    doc_source_meta_list = TextField(
        css_select="p.profile_meta>span.profile_meta_value", many=True, default=["", ""]
    )
    # 核心html
    doc_core_html = HtmlField(css_select="div#js_content", default="")
    # 公众号昵称
    doc_source_account_nick = ""
    # 公众号介绍
    doc_source_account_intro = ""
    # 文本内容，兼容
    doc_content = ""
    # 文章类型
    doc_type = "wechat"

    async def clean_doc_source_meta_list(self, value: list):
        """从doc_source_meta_list提取公众号昵称和介绍"""
        self.doc_source_account_nick = value[0]
        self.doc_source_account_intro = value[1]
        return value

    async def clean_doc_core_html(self, value: str):
        """清洗核心html"""

        return text_compress(
            str(value)
            .strip()
            .replace("visibility: visible;", "")
            .replace("<br>", "")
            .replace("data-src", "src")
        )

    async def clean_doc_date(self, value):
        """
        清洗时间，数据格式 2021-12-17 08:48
        """
        try:
            value = ts_to_str_date(value)
        except Exception as _:
            value = ts_to_str_date(time.time())
        return value

    async def clean_doc_ts(self, value):
        """
        清洗时间戳，数据格式1620567960
        """
        try:
            value = int(value)
        except Exception as _:
            value = int(time.time())
        return value

    # async def clean_doc_date(self, value):
    #     """
    #     清洗时间，数据格式 2021-12-17 08:48
    #     """
    #     if value:
    #         value += ":00"
    #     else:
    #         value = ts_to_str_date(time.time())
    #     return value

    # async def clean_doc_ts(self, value):
    #     """
    #     清洗时间戳，数据格式1620567960
    #     """
    #     if value:
    #         value += ":00"
    #     else:
    #         value = ts_to_str_date(time.time())
    #     # 转成时间数组
    #     time_arr = time.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    #     # 转时间戳
    #     ts = time.mktime(time_arr)
    #     return ts

    # async def clean_doc_date_f1(self, value):
    #     """
    #     清洗时间，数据格式 2021-12-17 08:48
    #     """
    #     return await self.clean_doc_date(value)

    # async def clean_doc_ts_f1(self, value):
    #     """
    #     清洗时间戳，数据格式 1620567960
    #     """
    #     return await self.clean_doc_ts(value)


class WechatSpider(Spider):
    """微信文章爬虫"""

    name = "WechatSpider"
    start_urls = ["https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw"]
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 5}
    concurrency = 10
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response):
        html = await response.text()
        item = await WechatItem.get_item(html=html)
        # print(item.results)
        print(item.doc_ts)
        print(item.doc_date)
        print(item.doc_des)
        yield item


if __name__ == "__main__":
    WechatSpider.start(middleware=ua_middleware)
