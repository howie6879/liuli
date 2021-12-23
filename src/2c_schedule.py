#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：统一调度入口
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: pipenv run pro or PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/2c_schdule.py
    - 调度时间：每日的 "00:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"
    Changelog: all notable changes to this file will be documented
"""
import time

import schedule

from src.schedule_task.all_tasks import send_doc, update_ads_tag, update_wechat_doc
from src.utils import LOGGER


def schedule_task():
    """
    更新持久化订阅的公众号最新文章
    :return:
    """
    # 抓取最新的文章，然后持久化到数据库
    update_wechat_doc()
    # 更新广告标签
    update_ads_tag()
    # 文章分发
    send_doc()


def main():
    """调度启动函数"""
    # 每日抓取公众号最新文章并更新广告标签
    schdule_time_list = ["00:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    for each in schdule_time_list:
        schedule.every().day.at(each).do(schedule_task)
    LOGGER.info("Schedule started successfully :)")
    schdule_msg = "Schedule time:\n " + "\n ".join(schdule_time_list)
    LOGGER.info(schdule_msg)
    # 启动就执行一次
    schedule_task()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
