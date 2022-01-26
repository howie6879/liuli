"""
    Created by howie.hu at 2022-01-21.
    Description: 执行分发动作
        - 执行命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/sender/action.py
    Changelog: all notable changes to this file will be documented
"""
import time

from src.config import Config
from src.databases import MongodbManager
from src.sender.send_factory import send_factory
from src.utils.log import LOGGER


def send_doc(sender_conf: dict):
    """
    对文章进行分发
    Args:
        sender_conf (dict): 分发配置
    """
    sender_list = sender_conf["sender_list"]
    query_days = sender_conf.get("query_days", 2)
    delta_time = sender_conf.get("delta_time", 3)
    skip_ads = sender_conf.get("skip_ads", False)
    if sender_list:
        # 是否启用分发器
        mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
        coll = mongo_base.get_collection(coll_name="liuli_articles")
        cur_ts = int(time.time())
        filter_dict = {
            # 时间范围，除第一次外后面其实可以去掉
            "doc_ts": {"$gte": cur_ts - (query_days * 24 * 60 * 60), "$lte": cur_ts},
        }
        if skip_ads:
            filter_dict.update(
                {
                    # 至少打上一个模型标签
                    "cos_model": {"$exists": True},
                    # 判定结果为非广告
                    "cos_model.result": 1,
                }
            )
        # 查找所有可分发文章
        for each_data in coll.find(filter_dict):
            # 分别分发给各个目标
            for send_type in sender_list:
                # 暂时固定，测试
                init_config = sender_conf.get(f"{send_type}_init_config", {})
                cos_model_resp = each_data.get("cos_model", {})
                doc_cus_des = ""
                if cos_model_resp:
                    # 经过模型判断
                    if cos_model_resp["result"] == 1:
                        # 广告标记
                        doc_cus_des = f"👿广告[概率：{cos_model_resp['probability']}]"
                    else:
                        doc_cus_des = "🤓非广告"

                each_data["doc_cus_des"] = doc_cus_des
                # 每次分发休眠一定时间
                time.sleep(delta_time)
                send_factory(
                    send_type=send_type, init_config=init_config, send_data=each_data
                )
    else:
        LOGGER.warn("未配置分发器!")


if __name__ == "__main__":
    send_config = {
        "sender_list": ["wecom"],
        "query_days": 7,
        "skip_ads": False,
        "delta_time": 3,
    }
    send_doc(send_config)
