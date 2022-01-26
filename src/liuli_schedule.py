#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：统一调度入口
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: pipenv run pro_schedule or PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/liuli_schedule.py
    - 调度时间：每日的 ["00:10", "12:10", "21:10"]
    Changelog: all notable changes to this file will be documented
"""
import json
import os
import time

import schedule

from src.backup.action import backup_doc
from src.collector.collect_factory import collect_factory
from src.config.config import Config
from src.processor import processor_dict
from src.sender.action import send_doc
from src.utils import LOGGER


def schedule_task(ll_config: dict):
    """更新持久化订阅的公众号最新文章

    Args:
        ll_config (dict): Liuli 任务配置
    """
    # 采集器配置
    collector_conf: dict = ll_config["collector"]
    # 处理器配置
    processor_conf: dict = ll_config["processor"]
    # 分发器配置
    sender_conf: dict = ll_config["sender"]
    # 备份器配置
    backup_conf: dict = ll_config["backup"]

    # 采集器执行
    LOGGER.info("采集器开始执行!")
    for collect_type, collect_config in collector_conf.items():
        collect_factory(collect_type, collect_config)
    LOGGER.info("采集器执行完毕!")
    # 采集器执行
    LOGGER.info("处理器(after_collect): 开始执行!")
    for each in processor_conf["after_collect"]:
        func_name = each.pop("func")
        LOGGER.info(f"处理器(after_collect): {func_name} 正在执行...")
        processor_dict[func_name](**each)
    LOGGER.info("处理器(after_collect): 执行完毕!")
    # 分发器执行
    LOGGER.info("分发器开始执行!")
    send_doc(sender_conf)
    LOGGER.info("分发器执行完毕!")
    # 备份器执行
    LOGGER.info("备份器开始执行!")
    backup_doc(backup_conf)
    LOGGER.info("备份器执行完毕!")


def start(ll_config_name: str = "default"):
    """调度启动函数

    Args:
        task_config (dict): 调度任务配置
    """
    ll_config_path = os.path.join(Config.LL_CONFIG_DIR, f"{ll_config_name}.json")
    with open(ll_config_path, "r", encoding="utf-8") as load_f:
        task_config = json.load(load_f)

    # 每日抓取公众号最新文章并更新广告标签
    schdule_time_list = task_config["schedule"].get(
        "period_list", ["00:10", "12:10", "21:10"]
    )
    for each in schdule_time_list:
        schedule.every().day.at(each).do(schedule_task, task_config)
    start_info = f"Schedule({Config.SCHEDULE_VERSION}) started successfully :)"
    LOGGER.info(start_info)
    schdule_msg = "Schedule time:\n " + "\n ".join(schdule_time_list)
    LOGGER.info(schdule_msg)
    # 启动就执行一次
    schedule_task(task_config)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start()
