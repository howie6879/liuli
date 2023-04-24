"""
    Created by howie.hu at 2022-01-05.
    Description: 采集器常用函数
    Changelog: all notable changes to this file will be documented
"""
import time

from copy import deepcopy

from src.config import Config
from src.databases.mongodb_base import MongodbManager
from src.databases.mongodb_tools import mongodb_update_data
from src.utils.log import LOGGER


def load_data_to_articlles(input_data: dict):
    """
    将获取的文章数据并持久化到 liuli_articles
    """
    # 抓取状态
    flag = False
    doc_source_name = input_data.get("doc_source_name")
    doc_source = input_data.get("doc_source")
    doc_name = input_data.get("doc_name")

    copy_input_data = deepcopy(input_data)
    copy_input_data["doc_ts"] = int(copy_input_data.get("doc_ts", int(time.time())))
    if doc_source_name and doc_source and doc_name:
        # 抓取成功进行持久化
        mongo_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        coll_conn = mongo_base.get_collection(coll_name="liuli_articles")
        filter_dict = {"doc_id": copy_input_data["doc_id"]}
        update_data = {"$set": copy_input_data}
        db_res = mongodb_update_data(
            coll_conn=coll_conn,
            filter_dict=filter_dict,
            update_data=update_data,
            upsert=True,
        )
        if db_res["status"]:
            msg = f"来自 {doc_source} 的文章持久化成功! 👉 {doc_source_name}: {doc_name} "
            flag = True
        else:
            msg = f"来自 {doc_source} 的文章持久化失败! 👉 {doc_source_name} {db_res['info']}"
    else:
        msg = f"来自 {doc_source} 的文章抓取失败! 👉 {doc_source}/{doc_source_name}/{doc_name} "
    LOGGER.info(msg)
    return flag
