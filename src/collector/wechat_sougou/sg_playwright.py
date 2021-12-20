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

from os import path

from playwright.async_api import async_playwright
from ruia import AttrField, Item, TextField

from src.utils.log import LOGGER


class SGWechatItem(Item):
    """
    搜索微信公众号页面信息提取类，一般是只会有一个结果
    示例：https://weixin.sogou.com/weixin?query=小众
    """

    # 默认此页面是多行内容列表
    target_item = TextField(css_select="div.news-box>ul>li")
    wechat_name = TextField(css_select="p.tit>a")
    wechat_id = TextField(css_select='label[name="em_weixinhao"]')
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


async def playwright_main(wechat_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # 进行公众号检索
        await page.goto("https://weixin.sogou.com/")
        await page.click('input[name="query"]')
        await page.fill('input[name="query"]', wechat_name)
        await page.click("text=搜公众号")
        await page.wait_for_load_state()
        # 抓取最新文章标题
        sg_html_handle = await page.query_selector("html")
        sg_html = await sg_html_handle.inner_html()
        if sg_html:
            item_list = []
            async for item in SGWechatItem.get_items(html=sg_html):
                item_list.append(item)
            if item_list:
                target_item = item_list[0]
                if target_item.wechat_name == wechat_name:
                    # 名字匹配才继续
                    LOGGER.info(
                        f"playwright 匹配公众号 {wechat_name}({target_item.wechat_id}) 成功! 正在提取最新文章: {target_item.latest_title}"
                    )
                    latest_href = target_item.latest_href

                    await page.goto(latest_href)
                    await page.wait_for_timeout(3000)
                    await page.wait_for_load_state()
                    print(await page.title())
                    wx_html_handle = await page.query_selector("html")
                    wx_html = await wx_html_handle.inner_html()
                    print(wx_html)

                    await page.pause()

        else:
            LOGGER.error(f"playwright 抓取 HTML 失败: {wechat_name} ")

        await browser.close()


if __name__ == "__main__":
    wechat_name = "老胡的储物柜"
    asyncio.run(playwright_main(wechat_name))
