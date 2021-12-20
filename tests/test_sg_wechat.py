"""
    Created by howie.hu at 2021-12-20.
    Description: 测试用例
        - pytest -s tests/test_sg_wechat.py
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import os

from src.collector.wechat_sougou.sg_playwright import SGWechatItem
from src.config import Config

ROOT_DIR = os.path.dirname(Config.BASE_DIR)
TEST_DIR = os.path.join(ROOT_DIR, "tests")


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
        print(item)
    return item_list


def test_sg_wechat_single_item():
    """测试 SGWechatItem 单行"""
    html_dir = os.path.join(TEST_DIR, "html_demo")
    html_path = os.path.join(html_dir, "single.html")
    HTML = ""
    with open(html_path, mode="r", encoding="utf-8") as file:
        HTML = file.read()
    res = asyncio.run(call_sg_item(HTML))
    assert res[0].wechat_name == "老胡的储物柜"
    assert res[0].latest_title == "我的周刊(第018期)"


def test_sg_wechat_multiple_item():
    """测试 SGWechatItem 多行"""
    html_dir = os.path.join(TEST_DIR, "html_demo")
    html_path = os.path.join(html_dir, "multiple.html")
    HTML = ""
    with open(html_path, mode="r", encoding="utf-8") as file:
        HTML = file.read()
    res = asyncio.run(call_sg_item(HTML))
    assert res[0].wechat_name == "Python编程"
    assert res[0].latest_title == "漫画|结对编程实在太可怕了!!"
