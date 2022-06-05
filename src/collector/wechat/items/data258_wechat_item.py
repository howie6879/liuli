"""
    Created by howie.hu at 2022-06-05.
    Description: 基于 Ruia 爬虫框架的 data258 微信页面 Item 提取类
    Changelog: all notable changes to this file will be documented
"""

from ruia import AttrField, Item, TextField


class Data258WechatItem(Item):
    """
    微阅读公众号搜索一级页面信息提取
    示例：https://mp.data258.com/mp/search?type=category&key=老胡的储物柜&sort=
    """

    target_item = TextField(css_select="div.layui-panel")
    wechat_name = TextField(css_select="h2>a", default="")
    wehcat_href = AttrField(css_select="h2>a", attr="href", default="")


class Data258WechatListItem(Item):
    """
    微阅读公众号历史文章信息提取
    示例: https://mp.data258.com/article/category/howie_locker
    """

    target_item = TextField(css_select="ul.jie-row>li")
    w_article_title = TextField(css_select="a.jie-title", default="")
    w_article_href = AttrField(css_select="a.jie-title", attr="href", default="")

    async def clean_w_article_title(self, value: list):
        """获取文章标题"""
        return str(value).strip() if value else ""
