"""
    Created by howie.hu at 2022-05-12.
    Description: 基于Ruia爬虫框架的微信公众号爬虫
        原始数据来源于：https://mp.data258.com/mp/search?type=category&key=老胡的储物柜&sort=
        ! 注意，该目标网站有比较严厉的反爬措施，单IP只能访问15次，此功能需要代理池
        - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: PIPENV_DOTENV_LOCATION=./dev.env pipenv run python src/collector/wechat/data258_ruia_start.py
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

from urllib.parse import urljoin

import execjs

from ruia import Response, Spider
from ruia_ua import middleware as ua_middleware

from src.collector.utils import load_data_to_articlles
from src.collector.wechat.items import (
    Data258WechatItem,
    Data258WechatListItem,
    WechatItem,
)
from src.processor import html_to_text_h2t
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption


def exec_js_data258(html: str) -> str:
    """返回js执行结果"""
    t_list = re.findall(r"setTimeout\(function\(\){(.*?);},", html)
    mp_res_list = []
    for i in t_list:
        js_text = """
        window = {};
        location = {
        href: null,
        };
        """
        js_text += re.compile(r"\}\);(.*?)</script>", re.S).search(html)[1]
        js_text += i
        js = execjs.compile(js_text)
        res = js.eval("location")["href"]
        if "www.data258.com" in res:
            break
        else:
            mp_res_list.append(res)

    return mp_res_list[-1] if mp_res_list else None


class Data258WechatSpider(Spider):
    """微信文章爬虫"""

    name = "Data258WechatSpider"
    request_config = {"RETRIES": 3, "DELAY": 3, "TIMEOUT": 10}
    concurrency = 1
    base_url = "https://mp.data258.com/"
    wechat_name = ""
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response: Response):
        """解析公众号原始链接数据"""
        html = await response.text()
        async for item in Data258WechatItem.get_items(html=html):
            if item.wechat_name == self.wechat_name:
                url = urljoin(self.base_url, item.wehcat_href)
                yield self.request(
                    url=url,
                    callback=self.parse_wechat_articles,
                )
                break

    async def parse_wechat_articles(self, response: Response):
        """解析公众号详情页面，提取历史文章"""
        html = await response.text()

        async for item in Data258WechatListItem.get_items(html=html):
            url = urljoin(self.base_url, item.w_article_href)
            yield self.request(
                url=url,
                headers={"Host": "mp.data258.com", "Referer": response.url},
                callback=self.parse_wechat_url,
                metadata={"wechat_title": item.w_article_title},
            )

    async def parse_wechat_url(self, response: Response):
        """解析公众号文章原始链接"""
        html = await response.text()
        if "今日浏览次数已达上限" in html:
            LOGGER.error(f"微信真实链接提取失败(IP 限制)：{response.metadata['wechat_title']} ")
        else:
            real_wechat_url = await asyncio.coroutine(exec_js_data258)(html)
            if real_wechat_url:
                yield self.request(
                    url=real_wechat_url,
                    callback=self.parse_wechat,
                )
            else:
                LOGGER.error(f"微信真实链接提取失败(js解密)：{response.metadata['wechat_title']} ")

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
                "doc_source": wechat_item.doc_source,
                "doc_source_account_nick": wechat_item.doc_source_account_nick,
                "doc_source_account_intro": wechat_item.doc_source_account_intro,
                "doc_content": html_to_text_h2t(html),
                "doc_html": "",
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
        Data258WechatSpider.wechat_name = wechat_name
        Data258WechatSpider.request_config = {
            "RETRIES": 3,
            "DELAY": delta_time,
            "TIMEOUT": 5,
        }
        t_url = (
            f"https://mp.data258.com/mp/search?type=category&key={wechat_name}&sort="
        )
        Data258WechatSpider.start_urls = [t_url]
        try:
            Data258WechatSpider.start(middleware=ua_middleware)
            s_nums += 1
        except Exception as e:
            err_msg = f"😿 公众号->{wechat_name} 文章更新失败! 错误信息: {e}"
            LOGGER.error(err_msg)

    msg = f"🤗 微信公众号文章更新完毕({s_nums}/{len(wechat_list)})!"
    LOGGER.info(msg)


if __name__ == "__main__":
    t_collect_config = {"wechat_list": ["老胡的储物柜"], "delta_time": 5}
    run(t_collect_config)
    # wechat_name = "老胡的储物柜"
    # t_url = f"https://mp.data258.com/mp/search?type=category&key={wechat_name}&sort="
    # Data258WechatSpider.start_urls = [t_url]
    # Data258WechatSpider.wechat_name = wechat_name
    # Data258WechatSpider.start(middleware=ua_middleware)
