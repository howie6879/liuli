"""
    Created by howie.hu at 2021-12-20.
    Description: 利用 playwright 模拟浏览器进行数据抓取，此脚本产出目标页HTML
        - 文档: https://playwright.dev/python/docs/intro
        - 安装: 默认使用 playwright 爬虫版本，如果要启用，请自行安装以下依赖
            - pipenv install playwright
            - playwright install chromium
            - playwright codegen https://weixin.sogou.com/
        - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
            - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/wechat_sougou/sg_playwright.py
        - 格式：
            {
                "doc_author": "howie6879",
                "doc_content": "",
                "doc_date": "2022-01-04 22:30",
                "doc_des": "老胡的周刊2021年合集~已经20期周刊了",
                "doc_id": "c7794ae61b31ab3a104a217f0ba722ae",
                "doc_image": "http://mmbiz.qpic.cn/mmbiz_jpg/YRBRJvZXcIWmjlTwwdYSdZJbqRf4XdgYXxsXWqmjcTkC23MlyyribSoeOy1OZCLYoSsJG75Qz4MKVdsibvNUBKiaw/0?wx_fmt=jpeg",
                "doc_link": "https://mp.weixin.qq.com/s?",
                "doc_name": "老胡的周刊2021年度汇总|附PDF下载",
                "doc_source": "liuli_wechat",
                "doc_source_account_intro": "编程、兴趣、生活",
                "doc_source_account_nick": "howie_locker",
                "doc_source_name": "老胡的储物柜",
                "doc_ts": 1641306600,
                "doc_type": "article"
            }
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import time

from playwright.async_api import async_playwright

from src.collector.utils import load_data
from src.collector.wechat_sougou.items import SGWechatItem, WechatItem
from src.common.process import html_to_text_h2t
from src.config.config import Config
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption


def run(collect_config: dict):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    s_nums = 0
    wechat_list = collect_config["wechat_list"]
    delta_time = collect_config.get("delta_time", 5)
    for name in wechat_list:
        time.sleep(delta_time)
        input_data = asyncio.run(playwright_main(name))
        # 持久化，必须执行
        flag = load_data(input_data)
        if flag:
            s_nums += 1
    msg = f"🤗 微信公众号文章更新完毕({s_nums}/{len(wechat_list)})"
    LOGGER.info(msg)


async def playwright_main(wechat_name: str):
    """利用 playwright 获取公众号元信息，输出数据格式见上方
    Args:
        wechat_name ([str]): 公众号名称
    """
    wechat_data = {}
    try:
        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=False)
            browser = await p.chromium.launch()
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
            )
            page = await context.new_page()
            # 进行公众号检索
            await page.goto("https://weixin.sogou.com/")
            await page.wait_for_load_state()
            await page.click('input[name="query"]')
            await page.fill('input[name="query"]', wechat_name)
            await asyncio.sleep(1)
            await page.click("text=搜公众号")
            await page.wait_for_load_state()
            # await page.pause()
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
                        info = f"playwright 匹配公众号 {wechat_name}({target_item.wechat_id}) 成功! 正在提取最新文章: {target_item.latest_title}"
                        LOGGER.info(info)
                        latest_href = target_item.latest_href

                        await page.goto(latest_href)
                        # 等待公众号图片加载出来，整个就算加载完毕
                        try:
                            await page.wait_for_selector(
                                selector="#js_pc_qr_code_img", timeout=6000
                            )
                        except Exception as _:
                            pass
                        await page.wait_for_load_state()
                        wx_html_handle = await page.query_selector("html")
                        wx_html = await wx_html_handle.inner_html()
                        wechat_item: WechatItem = await WechatItem.get_item(
                            html=wx_html
                        )
                        # 获取当前微信公众号文章地址
                        wechat_item.doc_link = page.url
                        doc_source_name = wechat_item.doc_source_name or wechat_name
                        wechat_data = {
                            **wechat_item.results,
                            **{
                                "doc_id": md5_encryption(
                                    f"{wechat_item.doc_name}_{doc_source_name}"
                                ),
                                "doc_source_name": doc_source_name,
                                "doc_link": wechat_item.doc_link,
                                "doc_source": wechat_item.doc_source,
                                "doc_source_account_nick": wechat_item.doc_source_account_nick,
                                "doc_source_account_intro": wechat_item.doc_source_account_intro,
                                "doc_content": html_to_text_h2t(wx_html),
                            },
                        }
                    else:
                        info = f"playwright 匹配公众号 {wechat_name} - {target_item.wechat_name} 失败! "
                        LOGGER.error(info)
            else:
                info = f"playwright 抓取 HTML 失败: {wechat_name} "
                LOGGER.error(info)
            await browser.close()
    except Exception as e:
        info = f"playwright 抓取出错: {wechat_name} str{e}"
        LOGGER.error(info)
    return wechat_data


if __name__ == "__main__":
    from pprint import pprint

    Config.WECHAT_LIST = ["老胡的储物柜"]
    for name in Config.WECHAT_LIST:
        time.sleep(2)
        res = asyncio.run(playwright_main("老胡的储物柜"))
        pprint(res)
