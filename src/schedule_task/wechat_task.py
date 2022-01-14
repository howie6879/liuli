#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：常用调度函数
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/schedule_task/all_tasks.py
    Changelog: all notable changes to this file will be documented
"""
import time

from src.classifier import model_predict_factory
from src.collector.collect_factory import collect_factory
from src.config import Config
from src.databases import MongodbManager
from src.processor import fetch_keyword_list
from src.sender import send_factory
from src.utils.log import LOGGER


def update_wechat_doc():
    """
    抓取最新的文章，然后持久化到数据库
    :param wechat_list:
    :return:
    """
    # TODO 统一的地方进行配置管理
    t_collect_type = "wechat_sougou"
    t_collect_config = {
        "wechat_list": Config.WECHAT_LIST,
        "delta_time": 5,
        # playwright
        "spider_type": "playwright",
    }
    collect_factory(t_collect_type, t_collect_config)


def update_ads_tag(is_force=False):
    """
    对订阅的文章进行广告标记
    :param is_force: 是否强制重新判决
    :return:
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="liuli_articles")
    if is_force:
        query = {}
    else:
        query = {"cos_model": {"$exists": False}}

    # 查找没有被标记的文章，基于相似度模型进行判断
    for each_data in coll.find(query):
        doc_name = each_data["doc_name"]
        doc_link = each_data["doc_link"]
        doc_source_name = each_data["doc_source_name"]
        doc_content = each_data["doc_content"]
        doc_keywords = each_data.get("doc_keywords")

        if not doc_keywords:
            keyword_list = fetch_keyword_list(doc_content)
            doc_keywords = " ".join(keyword_list)
            each_data["doc_keywords"] = doc_keywords

        # 基于余弦相似度
        cos_model_resp = model_predict_factory(
            model_name="cos",
            model_path="",
            input_dict={"text": doc_name + doc_keywords, "cos_value": Config.COS_VALUE},
            # input_dict={"text": doc_name, "cos_value": Config.COS_VALUE},
        ).to_dict()
        each_data["cos_model"] = cos_model_resp
        if cos_model_resp["result"] == 1:
            LOGGER.info(
                f"[{doc_source_name}] {doc_name} 被识别为广告[{cos_model_resp['probability']}]，链接为：{each_data['doc_link']}"
            )
        coll.update_one(
            filter={"doc_id": each_data["doc_id"]},
            update={"$set": each_data},
            upsert=True,
        )


def send_doc():
    """
    对文章进行分发
    :return:
    """
    if Config.SENDER_LIST:
        # 是否启用分发器
        mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
        coll = mongo_base.get_collection(coll_name="liuli_articles")
        cur_ts = time.time()
        filter_dict = {
            # 时间范围，除第一次外后面其实可以去掉
            "doc_ts": {"$gte": cur_ts - (2 * 24 * 60 * 60), "$lte": cur_ts},
            # 至少打上一个模型标签
            "cos_model": {"$exists": True},
        }
        # 查找所有可分发文章
        for each_data in coll.find(filter_dict):
            # 分别分发给各个目标
            for send_type in Config.SENDER_LIST:
                # 暂时固定，测试
                send_config = {}
                each_data["doc_cus_des"] = "🤓非广告"
                cos_model_resp = each_data["cos_model"]
                if cos_model_resp["result"] == 1:
                    # 广告标记
                    each_data[
                        "doc_cus_des"
                    ] = f"👿广告[概率：{cos_model_resp['probability']}]"
                send_factory(
                    send_type=send_type, send_config=send_config, send_data=each_data
                )
    else:
        LOGGER.info("未配置分发器!")


if __name__ == "__main__":
    # 第一次启动请执行
    # update_wechat_doc()
    # 每次强制重新打标签
    # update_ads_tag(is_force=False)
    send_doc()
