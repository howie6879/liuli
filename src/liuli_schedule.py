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

from multiprocessing import Pool, freeze_support

import schedule

from src.backup.action import backup_doc
from src.collector.collect_factory import collect_factory
from src.config.config import Config
from src.processor import processor_dict
from src.sender.action import send_doc
from src.utils import LOGGER


def run_liuli_task(ll_config: dict):
    """执行调度任务

    Args:
        ll_config (dict): Liuli 任务配置
    """
    # 文章源, 用于基础查询条件
    doc_source: str = ll_config["doc_source"]
    basic_filter = {"basic_filter": {"doc_source": doc_source}}
    # 采集器配置
    collector_conf: dict = ll_config["collector"]
    # 处理器配置
    processor_conf: dict = ll_config["processor"]
    # 分发器配置
    sender_conf: dict = ll_config["sender"]
    sender_conf.update(basic_filter)
    # 备份器配置
    backup_conf: dict = ll_config["backup"]
    backup_conf.update(basic_filter)

    # 采集器执行
    LOGGER.info("采集器开始执行!")
    for collect_type, collect_config in collector_conf.items():
        collect_factory(collect_type, collect_config)
    LOGGER.info("采集器执行完毕!")
    # 采集器执行
    LOGGER.info("处理器(after_collect): 开始执行!")
    for each in processor_conf["after_collect"]:
        func_name = each.pop("func")
        # 注入查询条件
        each.update(basic_filter)
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


def run_liuli_schedule(ll_config_name: str = "default"):
    """调度启动函数

    Args:
        task_config (dict): 调度任务配置
    """
    ll_config_path = os.path.join(Config.LL_CONFIG_DIR, f"{ll_config_name}.json")
    with open(ll_config_path, "r", encoding="utf-8") as load_f:
        ll_config = json.load(load_f)

    schdule_time_list = ll_config["schedule"].get(
        "period_list", ["00:10", "12:10", "21:10"]
    )
    for each in schdule_time_list:
        schedule.every().day.at(each).do(run_liuli_task, ll_config)

    name: str = ll_config["name"]
    author: str = ll_config["author"]
    start_info = f"Schedule({Config.SCHEDULE_VERSION}) task({name}@{author}) started successfully :)"
    LOGGER.info(start_info)
    schdule_msg = f"Task({name}@{author}) schedule time:\n " + "\n ".join(
        schdule_time_list
    )
    LOGGER.info(schdule_msg)
    # 启动就执行一次
    run_liuli_task(ll_config)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start(ll_config_name: str = ""):
    """调度启动函数

    Args:
        task_config (dict): 调度任务配置
    """
    if not ll_config_name:
        freeze_support()

        # 默认启动 liuli_config 目录下所有配置
        ll_config_name_list = []
        for each_file in os.listdir(Config.LL_CONFIG_DIR):
            if each_file.endswith("json"):
                # 加入启动列表
                ll_config_name_list.append(each_file.replace(".json", ""))
        # 进程池
        p = Pool(len(ll_config_name_list))
        for each_ll_config_name in ll_config_name_list:
            LOGGER.info(f"Task {each_ll_config_name} register successfully!")
            p.apply_async(run_liuli_schedule, args=(each_ll_config_name,))
        p.close()
        p.join()

    else:
        run_liuli_schedule(ll_config_name)


if __name__ == "__main__":
    start(ll_config_name="")
