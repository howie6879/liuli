"""
    Created by howie.hu at 2022-01-14.
    Description: 搜狗微信爬虫启动函数
    Changelog: all notable changes to this file will be documented
"""


def run(collect_config: dict):
    """微信公众号文章抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    spider_type = collect_config.get("spider_type", "ruia")
    if spider_type == "ruia" or spider_type == "sg_ruia":
        from src.collector.wechat.sg_ruia_start import run as ruia_run

        run_func = ruia_run
    elif spider_type == "playwright" or spider_type == "sg_playwright":
        from src.collector.wechat.sg_playwright_start import run as playwright_run

        run_func = playwright_run
    elif spider_type == "feeddd":
        from src.collector.wechat.feeddd_start import run as feeddd_run

        run_func = feeddd_run
    elif spider_type == "data258":
        from src.collector.wechat.data258_ruia_start import run as data258_run

        run_func = data258_run
    else:
        run_func = ruia_run

    # 启动
    run_func(collect_config)
