"""
    Created by howie.hu at 2021-12-21.
    Description: 基于 Ruia 的搜狗微信页面 Item 提取类
    Changelog: all notable changes to this file will be documented
"""

from ruia import AttrField, Item, TextField


class SGWechatItem(Item):
    """
    搜索搜狗微信公众号页面信息提取类，一般是只会有一个结果
    示例：https://weixin.sogou.com/weixin?query=老胡的储物柜
    """

    # 默认此页面是多行内容列表
    target_item = TextField(css_select="div.news-box>ul>li")
    wechat_name = TextField(css_select="p.tit>a", default="")
    wechat_id = TextField(css_select='label[name="em_weixinhao"]', default="")
    latest_title = TextField(css_select='dd>a[target="_blank"]', default="暂无更新")
    latest_href = AttrField(css_select='dd>a[target="_blank"]', attr="href", default="")

    async def clean_wechat_name(self, wechat_name: str) -> str:
        """
        清洗 wechat_name
        """
        return str(wechat_name).replace("\n", "").replace(" ", "").strip()

    async def clean_wechat_id(self, wechat_id: str) -> str:
        """
        清洗 wechat_id
        """
        return str(wechat_id).strip()

    async def clean_latest_title(self, latest_title: str) -> str:
        """
        清洗 latest_title
        """
        return str(latest_title).replace("\n", "").replace(" ", "").strip()

    async def clean_latest_href(self, latest_href: str) -> str:
        """
        清洗 latest_href
        """
        f_url = ""
        if latest_href:
            f_url = f"https://weixin.sogou.com/{latest_href}"
        return f_url
