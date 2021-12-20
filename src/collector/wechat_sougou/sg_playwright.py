"""
    Created by howie.hu at 2021-12-20.
    Description: 利用 playwright 模拟浏览器进行数据抓取，此脚本产出目标页HTML
        - 文档: https://playwright.dev/python/docs/intro
        - 安装
            - pipenv install playwright
            - playwright install chromium
            - playwright codegen https://weixin.sogou.com/
    Changelog: all notable changes to this file will be documented
"""

import asyncio

from playwright.async_api import async_playwright
from ruia import Item, TextField


class SGWechat(Item):
    """
    搜索微信公众号页面信息提取类，一般是只会有一个结果
    示例：https://weixin.sogou.com/weixin?query=小众
    """

    # 默认此页面是多行内容列表
    target_item = TextField(css_select="div.news-box li")
    title = TextField(css_select="p.tit>a")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # 进行公众号检索
        await page.goto("https://weixin.sogou.com/")
        await page.click('input[name="query"]')
        await page.fill('input[name="query"]', "小众消息")
        await page.click("text=搜公众号")
        await page.wait_for_load_state()
        # 抓取最新文章标题
        html_handle = await page.query_selector("html")
        html = await html_handle.inner_html()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
