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

from pprint import pprint

from playwright.async_api import async_playwright

from src.collector.wechat_sougou.sg_wechat_item import SGWechatItem
from src.collector.wechat_sougou.wechat_item import WechatItem
from src.utils.log import LOGGER


async def playwright_main(wechat_name: str):
    """利用 playwright 获取公众号元信息
    eg:
    {
        "doc_author": "howie6879",
        "doc_content": "",
        "doc_des": "本周推荐游戏程序员的读书笔记，致敬。",
        "doc_image": "http://mmbiz.qpic.cn/mmbiz_jpg/YRBRJvZXcIVBtU4gtNsZrRQtDLDS725uEGsCGXHbq7GzfDK2KumHOSKkA6TiaWLia1co96EzPqHRoiac7w7wtqlkg/0?wx_fmt=jpeg",
        "doc_keywords": [],
        "doc_link": "https://mp.weixin.qq.com/s?src=11&timestamp=1640181418&ver=3512&signature=ApU4NMdzDDuVlwcXb1VQ8ut-lNlUahMuEBid*ntpcvX68KXhxAEP1FPMLiSCmN6iM1QCGPRqf3AXPm8hmCnn3t4mwsWS0c6*kDuIqLQgHQX2eGn8jGo-qvgNPc1xJ*uZ&new=1",
        "doc_name": "我的周刊（第018期）",
        "doc_source": "2c_wechat",
        "doc_source_account_intro": "编程、兴趣、生活",
        "doc_source_account_nick": "howie_locker",
        "doc_source_meta_list": ["howie_locker", "编程、兴趣、生活"],
        "doc_source_name": "老胡的储物柜",
        "doc_type": "article",
    }
    Args:
        wechat_name ([str]): 公众号名称
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # browser = await p.chromium.launch()
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
                    # 等待公众号图片加载出来，整个就算加载完毕
                    await page.wait_for_selector("#js_pc_qr_code_img")
                    await page.wait_for_load_state()
                    wx_html_handle = await page.query_selector("html")
                    wx_html = await wx_html_handle.inner_html()
                    wechat_item: WechatItem = await WechatItem.get_item(html=wx_html)
                    # 获取当前微信公众号文章地址
                    wechat_item.doc_link = page.url
                    wechat_data = {
                        **wechat_item.results,
                        **{
                            "doc_link": wechat_item.doc_link,
                            "doc_source": wechat_item.doc_source,
                            "doc_source_account_nick": wechat_item.doc_source_account_nick,
                            "doc_source_account_intro": wechat_item.doc_source_account_intro,
                            "doc_content": wechat_item.doc_content,
                            "doc_keywords": wechat_item.doc_keywords,
                        },
                    }
                    pprint(wechat_data)

        else:
            LOGGER.error(f"playwright 抓取 HTML 失败: {wechat_name} ")
        await browser.close()


if __name__ == "__main__":
    wechat_name = "老胡的储物柜"
    asyncio.run(playwright_main(wechat_name))
