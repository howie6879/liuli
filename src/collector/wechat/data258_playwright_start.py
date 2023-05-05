"""
    Created by howie.hu at 2022-06-05.
    Description: 利用 playwright 模拟浏览器进行数据抓取微笑公众号
        - 文档: https://playwright.dev/python/docs/intro
        - 安装: 默认使用 playwright 爬虫版本，如果要启用，请自行安装以下依赖
            - pipenv install playwright
            - playwright install chromium
            - playwright codegen https://mp.data258.com/mp/search
        - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
            - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/wechat/data258_playwright_start.py
        - 格式：
    Changelog: all notable changes to this file will be documented
"""

import asyncio
import time

from urllib.parse import urljoin

from playwright.async_api import async_playwright

from src.collector.wechat.items import Data258WechatItem, Data258WechatListItem
from src.config import Config
from src.utils.log import LOGGER


def run(collect_config: dict = {}):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    asyncio.run(playwright_main("老胡的储物柜"))


async def playwright_main(wechat_name: str):
    """利用 playwright 获取公众号元信息，输出数据格式见上方
    Args:
        wechat_name ([str]): 公众号名称
    """
    base_url = "https://mp.data258.com/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=Config.LL_SPIDER_UA)
        page = await context.new_page()
        # # 关闭Webdriver属性

        js = """
        
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
        await page.add_init_script(js)
        # 进行公众号检索
        await page.goto(
            f"https://mp.data258.com/mp/search?type=category&key={wechat_name}&sort="
        )
        await page.wait_for_load_state()
        # window.navigator.webdriver
        wechat_name_html_handle = await page.query_selector("html")
        wechat_name_html = await wechat_name_html_handle.inner_html()
        await asyncio.sleep(1)
        async for item in Data258WechatItem.get_items(html=wechat_name_html):
            if item.wechat_name == wechat_name:
                details_url = urljoin(base_url, item.wehcat_href)
                # 名字匹配才继续
                info = f"playwright 匹配公众号 {wechat_name}({wechat_name}) 成功! 正在提取历史文章"
                LOGGER.info(info)
                # 获取详情页
                await page.goto(details_url)
                await page.wait_for_load_state()
                wechat_list_html_handle = await page.query_selector("html")
                wechat_list_html = await wechat_list_html_handle.inner_html()
                async for item in Data258WechatListItem.get_items(
                    html=wechat_list_html
                ):
                    article_url = urljoin(base_url, item.w_article_href)
                    w_article_title = item.w_article_title
                    print(item.results)
                    await page.add_init_script(js)
                    print(article_url)
                    await page.goto(article_url, referer=details_url)
                    await page.pause()
            else:
                info = f"playwright 匹配公众号 {wechat_name} 失败! "
                LOGGER.error(info)

        exit()


if __name__ == "__main__":
    run()
