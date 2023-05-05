"""
    Created by howie.hu at 2022-01-13.
    Description: 基于Ruia爬虫框架的微信公众号爬虫
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: PIPENV_DOTENV_LOCATION=./online.env pipenv run python src/collector/wechat/sg_ruia_start.py
        - 结果示例：
        {
            "doc_date": "2022-01-09 21:20:00",
            "doc_image": "wx_fmt=jpeg",
            "doc_name": "我的周刊（第021期）",
            "doc_ts": 1641734400,
            "doc_link": "",
            "doc_source_meta_list": [
                "howie_locker",
                "编程、兴趣、生活"
            ],
            "doc_des": "奇文共欣赏，疑义相与析",
            "doc_core_html": "hello world",
            "doc_type": "article",
            "doc_author": "howie6879",
            "doc_source_name": "老胡的储物柜",
            "doc_id": "3b6b3dd93b58164f0f60403b06ef689a",
            "doc_source": "liuli_wechat",
            "doc_source_account_nick": "howie_locker",
            "doc_source_account_intro": "编程、兴趣、生活",
            "doc_content": "hello world",
            "doc_keywords": ""
        }
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import re

from ruia import Response, Spider
from ruia_ua import middleware as ua_middleware

from src.collector.utils import load_data_to_articlles
from src.collector.wechat.items import SGWechatItem, WechatItem
from src.processor import html_to_text_h2t
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption


class SGWechatSpider(Spider):
    """微信文章爬虫"""

    name = "SGWechatSpider"
    request_config = {"RETRIES": 3, "DELAY": 3, "TIMEOUT": 5}
    concurrency = 10
    wechat_name = ""
    doc_source = ""
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response: Response):
        """解析公众号原始链接数据"""
        html = await response.text()
        item_list = []
        async for item in SGWechatItem.get_items(html=html):
            # 修复清洗空格造成公众号名称不相等Bug
            # 具体见：https://github.com/liuli-io/liuli/issues/60
            if (
                item.wechat_name
                == self.wechat_name.replace("\n", "").replace(" ", "").strip()
            ):
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
        wechat_data = {
            **wechat_item.results,
            **{
                "doc_id": md5_encryption(f"{wechat_item.doc_name}_{self.wechat_name}"),
                "doc_keywords": "",
                "doc_source_name": self.wechat_name,
                "doc_link": response.url,
                "doc_source": self.doc_source,
                "doc_source_account_nick": wechat_item.doc_source_account_nick,
                "doc_source_account_intro": wechat_item.doc_source_account_intro,
                "doc_content": html_to_text_h2t(html),
                "doc_html": "",
                "doc_type": wechat_item.doc_type,
            },
        }
        await asyncio.coroutine(load_data_to_articlles)(input_data=wechat_data)


def run(collect_config: dict):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    s_nums = 0
    wechat_list = collect_config["wechat_list"]
    delta_time = collect_config.get("delta_time", 3)
    for wechat_name in wechat_list:
        SGWechatSpider.wechat_name = wechat_name
        SGWechatSpider.doc_source = collect_config["doc_source"]
        SGWechatSpider.request_config = {
            "RETRIES": 3,
            "DELAY": delta_time,
            "TIMEOUT": 5,
        }
        t_url = f"https://weixin.sogou.com/weixin?type=1&query={wechat_name}&ie=utf8&s_from=input&_sug_=n&_sug_type_="
        SGWechatSpider.start_urls = [t_url]
        try:
            SGWechatSpider.start(middleware=ua_middleware)
            s_nums += 1
        except Exception as e:
            err_msg = f"😿 公众号->{wechat_name} 文章更新失败! 错误信息: {e}"
            LOGGER.error(err_msg)

    msg = f"🤗 微信公众号文章更新完毕({s_nums}/{len(wechat_list)})!"
    LOGGER.info(msg)


if __name__ == "__main__":
    t_collect_config = {
        "wechat_list": ["老胡的储物柜"],
        "delta_time": 10,
        "spider_type": "ruia",
        "doc_source": "liuli_wechat",
    }
    run(t_collect_config)

    # sg_url = "https://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&_sug_=n&_sug_type_="
    # SGWechatSpider.wechat_name = "老胡的储物柜"
    # SGWechatSpider.start_urls = [sg_url.format(SGWechatSpider.wechat_name)]
    # SGWechatSpider.start(middleware=ua_middleware)
