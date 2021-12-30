"""
    Created by howie.hu at 2021-12-20.
    Description: 测试用例
        - pytest -s tests/test_sg_wechat.py
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import os

from src.collector.wechat_sougou.items import SGWechatItem, WechatItem
from src.config import Config

ROOT_DIR = os.path.dirname(Config.BASE_DIR)
TEST_DIR = os.path.join(ROOT_DIR, "tests")
HTML_DIR = os.path.join(TEST_DIR, "html_demo")


async def call_sg_item(html: str) -> list:
    """调用搜狗Item类

    Args:
        html (str): HTML内容

    Returns:
        list: 返回结果列表
    """
    item_list = []
    async for item in SGWechatItem.get_items(html=html):
        item_list.append(item)
    return item_list


def read_html(html_name: str) -> str:
    """读取HTML目录下的相关文件

    Args:
        html_name (str): 文件名称

    Returns:
        str: HTML内容
    """
    html_path = os.path.join(HTML_DIR, html_name)
    HTML = ""
    with open(html_path, mode="r", encoding="utf-8") as file:
        HTML = file.read()
    return HTML


def test_wechat_item():
    """测试微信Item"""
    html = read_html(html_name="wechat_demo.html")
    item: WechatItem = asyncio.run(WechatItem.get_item(html=html))
    print(item)
    assert item.doc_source_name == "老胡的储物柜"
    assert item.doc_source_account_nick == "howie_locker"
    assert item.doc_source_account_intro == "编程、兴趣、生活"


def test_sg_wechat_single_item():
    """测试 SGWechatItem 单行"""
    html = read_html(html_name="single.html")
    res = asyncio.run(call_sg_item(html))
    assert res[0].wechat_name == "老胡的储物柜"
    assert res[0].latest_title == "我的周刊(第018期)"


def test_sg_wechat_multiple_item():
    """测试 SGWechatItem 多行"""
    html = read_html(html_name="multiple.html")
    res = asyncio.run(call_sg_item(html))
    assert res[0].wechat_name == "Python编程"
    assert res[0].latest_title == "漫画|结对编程实在太可怕了!!"
