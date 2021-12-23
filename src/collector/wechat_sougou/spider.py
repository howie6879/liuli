"""
    Created by howie.hu at 2021-12-23.
    Description: 微信文章爬虫主入口
    Changelog: all notable changes to this file will be documented
"""
import time

from src.collector.wechat_sougou.sg_playwright import load_data_from_playwright
from src.config import Config
from src.utils.log import LOGGER


def run_wechat_doc_spider(
    wechat_list: list = Config.WECHAT_LIST, delta_time: int = 0.5
):
    """微信公众号文章抓取爬虫

    Args:
        wechat_list (list, optional): 公众号列表. Defaults to Config.WECHAT_LIST.
        delta_time (int, optional): 公众号抓取间隔时间. Defaults to 0.5.
    """
    s_nums = 0
    for name in wechat_list:
        time.sleep(delta_time)
        flag = load_data_from_playwright(name)
        if flag:
            s_nums += 1
    msg = f"🤗 微信公众号文章更新完毕({s_nums}/{len(wechat_list)})"
    LOGGER.info(msg)
