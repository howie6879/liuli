#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：统一调度入口
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: pipenv run pro_schedule or pipenv run python src/liuli_schedule.py
    - 调度时间：每日的 ["00:10", "12:10", "21:10"]
    Changelog: all notable changes to this file will be documented
"""

import time

from copy import deepcopy
from multiprocessing import Process

import schedule

from src.backup.action import backup_doc
from src.collector.collect_factory import collect_factory
from src.common.db_utils import get_liuli_config
from src.config import Config, init_env_config
from src.databases import MongodbManager, mongodb_find
from src.processor import processor_dict
from src.sender.action import send_doc
from src.utils import LOGGER


def run_liuli_task(ll_config: dict):
    """执行调度任务

    Args:
        ll_config (dict): Liuli 任务配置
    """
    try:
        # 全局更新 Config 配置
        Config.set_config(get_liuli_config())
        # 防止内部函数篡改
        ll_config_data = deepcopy(ll_config)
        # 文章源, 用于基础查询条件
        doc_source: str = ll_config_data["doc_source"]
        basic_filter = {"basic_filter": {"doc_source": doc_source}}
        # 采集器配置
        collector_conf: dict = ll_config_data["collector"]
        # 处理器配置
        processor_conf: dict = ll_config_data["processor"]
        # 分发器配置
        sender_conf: dict = ll_config_data["sender"]
        sender_conf.update(basic_filter)
        # 备份器配置
        backup_conf: dict = ll_config_data["backup"]
        backup_conf.update(basic_filter)

        # 采集器执行
        LOGGER.info("采集器开始执行!")
        for collect_type, collect_config in collector_conf.items():
            collect_factory(
                collect_type, {**collect_config, **{"doc_source": doc_source}}
            )
        LOGGER.info("采集器执行完毕!")
        # 采集器执行
        LOGGER.info("处理器(after_collect): 开始执行!")
        for each in processor_conf["after_collect"]:
            func_name = each.get("func")
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
    except Exception as e:
        LOGGER.exception(f"执行失败！{e}")


def run_liuli_schedule(ll_config: dict):
    """调度启动函数

    Args:
        ll_config (dict): Liuli 任务配置
    """
    schdule_time_list = ll_config["schedule"].get(
        "period_list", ["00:10", "12:10", "21:10"]
    )
    for each in schdule_time_list:
        schedule.every().day.at(each).do(run_liuli_task, ll_config)

    name: str = ll_config["name"]
    author: str = ll_config["author"]
    start_info = (
        f"Schedule({Config.VERSION}) task({name}@{author}) started successfully :)"
    )
    LOGGER.info(start_info)
    schdule_msg = f"Schedule Task({name}@{author}) schedule time:\n " + "\n ".join(
        schdule_time_list
    )
    LOGGER.info(schdule_msg)
    # 启动就执行一次
    run_liuli_task(ll_config)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    """调度启动函数

    Args:
        doc_source (str): 调度任务配置
    """
    while True:
        LOGGER.info("Schedule start...")
        # 检查数据库集合 是否存在配置数据
        Config.LL_MONGODB_CONFIG = init_env_config()["mongodb"]
        mongodb_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        # 配置 liuli_doc_source 前，一定要配置好 liuli_config
        coll = mongodb_base.get_collection(coll_name="liuli_doc_source")
        db_res = mongodb_find(
            coll_conn=coll,
            filter_dict={"username": "liuli", "is_open": 1},
            return_dict={"_id": 0},
            sorted_list=[("doc_source", -1)],
        )
        db_info = db_res["info"]
        if db_res["status"]:
            if db_info:
                process_list = []
                for each_config in db_info:
                    process_list.append(
                        Process(target=run_liuli_schedule, args=(each_config,))
                    )

                _ = [p.start() for p in process_list]
                _ = [p.join() for p in process_list]
                break

        else:
            err_info = f"Schedule start failed! DB response info -> {db_info}"
            LOGGER.error(err_info)
        # 休眠 5 秒重试
        time.sleep(5)


if __name__ == "__main__":
    start()
