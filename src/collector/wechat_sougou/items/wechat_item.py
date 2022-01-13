"""
    Created by howie.hu at 2021-12-22.
    Description: 基于 Ruia 的微信页面 Item 提取类
    Changelog: all notable changes to this file will be documented
"""
import time

from ruia import AttrField, HtmlField, Item, RegexField, Spider, TextField
from ruia_ua import middleware as ua_middleware


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
    # 文章类型
    doc_type = AttrField(
        css_select='meta[property="og:type"]', attr="content", default=""
    )
    # 文章发布日期
    # doc_date = TextField(css_select="em#publish_time", default="")
    doc_date = RegexField(re_select=r"t=\"(20\d.*)\"\;", default="2099-01-01 00:00")
    # 文章发布时间戳
    # doc_ts = TextField(css_select="em#publish_time", default="")
    doc_ts = RegexField(re_select=r"t=\"(20\d.*)\"\;", default="2099-01-01 00:00")
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
    # 常量
    # 信息来源
    doc_source = "liuli_wechat"

    async def clean_doc_source_meta_list(self, value: list):
        """从doc_source_meta_list提取公众号昵称和介绍"""
        self.doc_source_account_nick = value[0]
        self.doc_source_account_intro = value[1]
        return value

    async def clean_doc_core_html(self, value: list):
        """清洗核心html"""

        return (
            str(value)
            .strip()
            .replace("visibility: visible;", "")
            .replace("<br>", "")
            .replace("data-src", "src")
        )

    async def clean_doc_ts(self, value):
        """
        清洗时间戳，数据格式 2021-12-17 08:48
        """
        # 转成时间数组
        time_arr = time.strptime(str(value), "%Y-%m-%d %H:%M")
        # 转时间戳
        ts = time.mktime(time_arr)
        return ts


class WechatSpider(Spider):
    """微信文章爬虫"""

    name = "WechatSpider"
    start_urls = ["https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw"]
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 20}
    concurrency = 10
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response):
        html = await response.text()
        item = await WechatItem.get_item(html=html)
        print(item.doc_core_html)
        yield item


if __name__ == "__main__":
    WechatSpider.start(middleware=ua_middleware)
