"""
    Created by howie.hu at 2022-01-21.
    Description: 执行分发动作
    Changelog: all notable changes to this file will be documented
"""
import time

from src.config import Config
from src.databases import MongodbManager
from src.sender.send_factory import send_factory
from src.utils.log import LOGGER


def send_doc():
    """
    对文章进行分发
    :return:
    """
    if Config.SENDER_LIST:
        # 是否启用分发器
        mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
        coll = mongo_base.get_collection(coll_name="liuli_articles")
        cur_ts = int(time.time())
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
        LOGGER.warn("未配置分发器!")
