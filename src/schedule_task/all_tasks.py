#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：常用调度函数
    Changelog: all notable changes to this file will be documented
"""
import time

from src.classifier import model_predict_factory
from src.collector.wechat import (
    run_wechat_doc_spider,
    run_wechat_name_spider,
    wechat2url,
)
from src.config import Config
from src.databases import MongodbManager
from src.sender import send_factory


def update_wechat_doc():
    """
    抓取最新的文章，然后持久化到数据库
    :param wechat_list:
    :return:
    """
    # TODO 统一的地方进行配置管理
    wechat_urls = wechat2url(Config.WECHAT_LIST)
    run_wechat_doc_spider(list(wechat_urls.values()))


def update_ads_tag():
    """
    对订阅的文章进行广告标记
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="2c_articles")
    # 查找没有被标记的文章，基于预先相似度模型进行判断
    for each_data in coll.find({"cos_model": {"$exists": False}}):
        doc_name = each_data["doc_name"]
        # 基于余弦相似度
        cos_model_resp = model_predict_factory(
            model_name="cos",
            model_path="",
            input_dict={"text": doc_name, "cos_value": 0.65},
        ).to_dict()
        each_data["cos_model"] = cos_model_resp
        if cos_model_resp["result"] == 1:
            print(
                f"{doc_name} 被识别为广告[{cos_model_resp['probability']}]，链接为：{each_data['doc_link']}"
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
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="2c_articles")
    cur_ts = time.time()
    filter_dict = {
        # 时间范围，除第一次外后面其实可以去掉
        "doc_ts": {"$gte": cur_ts - (1 * 24 * 60 * 60), "$lte": cur_ts},
        # 至少打上一个模型标签
        "cos_model": {"$exists": True},
    }
    # 查找所有可分发文章
    for each_data in coll.find(filter_dict):
        # 分别分发给各个目标
        for send_type in Config.SENDER_LIST:
            # 暂时固定，测试
            send_config = {"url": Config.DD_URL}
            each_data["doc_cus_des"] = "非广告"
            cos_model_resp = each_data["cos_model"]
            if cos_model_resp["result"] == 1:
                # 广告标记
                each_data[
                    "doc_cus_des"
                ] = f"广告[probability{cos_model_resp['probability']}]"
            send_factory(
                send_type=send_type, send_config=send_config, send_data=each_data
            )


if __name__ == "__main__":
    # 第一次启动请执行
    # run_wechat_name_spider()
    update_wechat_doc()
    update_ads_tag()
    send_doc()
