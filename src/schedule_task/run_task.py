#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：统一调度入口
    暂定时间：每日的
        - 07:10
        - 11:10
        - 13:10
        - 16:10
        - 20:10
        - 23:10
    Changelog: all notable changes to this file will be documented
"""


import time

import schedule

from src.collector.wechat import run_wechat_doc_spider
from src.schedule_task.ads_tag_task import ads_tag_update


def update_wechat_doc():
    """
    更新持久化订阅的公众号最新文章
    :return:
    """
    # 抓取最新的文章，然后持久化到数据库
    run_wechat_doc_spider()
    # 更新广告标签
    ads_tag_update()


if __name__ == "__main__":
    # 每日抓取公众号最新文章并更新广告标签
    schedule.every().day.at("07:10").do(update_wechat_doc)
    schedule.every().day.at("11:10").do(update_wechat_doc)
    schedule.every().day.at("16:10").do(update_wechat_doc)
    schedule.every().day.at("20:10").do(update_wechat_doc)
    schedule.every().day.at("23:10").do(update_wechat_doc)
    while True:
        schedule.run_pending()
        time.sleep(1)
