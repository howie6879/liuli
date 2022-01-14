"""
    Created by howie.hu at 2022-01-14.
    Description: 搜狗微信爬虫启动函数
    Changelog: all notable changes to this file will be documented
"""
from src.collector.wechat_sougou.playwright_start import playwright_main
from src.collector.wechat_sougou.playwright_start import run as playwright_run
from src.collector.wechat_sougou.ruia_start import run as ruia_run


def run(collect_config: dict):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    spider_type = collect_config.get("spider_type", "ruia")
    spider_type_run = {"ruia": ruia_run, "playwright": playwright_run}
    # 启动
    spider_type_run.get(spider_type, "ruia")(collect_config)
