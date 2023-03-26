"""
    Created by howie.hu at 2022-01-21.
    Description: 执行分发动作
        - 执行命令: PIPENV_DOTENV_LOCATION=./online.env pipenv run python src/sender/action.py
    Changelog: all notable changes to this file will be documented
"""
import time

from src.common.doc_utils import get_bak_doc_link
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
    link_source = sender_conf.get("link_source", "self")
    basic_filter = sender_conf.get("basic_filter", {})
    ignore_doc_source_name = sender_conf.get("ignore_doc_source_name", [])
    skip_ads = sender_conf.get("skip_ads", False)
    if sender_list:
        # 是否启用分发器
        mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
        coll = mongo_base.get_collection(coll_name="liuli_articles")

        # 分别分发给各个目标
        for send_type in sender_list:
            # 构建查询条件
            cur_ts = int(time.time())
            custom_filter = sender_conf.get("custom_filter", {}).get(send_type, {})
            query_days = custom_filter.get("query_days", query_days)
            delta_time = custom_filter.get("delta_time", delta_time)
            link_source = custom_filter.get("link_source", link_source)
            skip_ads = custom_filter.get("skip_ads", skip_ads)
            ignore_doc_source_name = custom_filter.get(
                "ignore_doc_source_name", ignore_doc_source_name
            )
            filter_dict = {
                **basic_filter,
                **{
                    # 时间范围，除第一次外后面其实可以去掉
                    "doc_ts": {
                        "$gte": cur_ts - (query_days * 24 * 60 * 60),
                        "$lte": cur_ts,
                    },
                    # 过滤文档源名称
                    "doc_source_name": {"$nin": ignore_doc_source_name},
                },
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
                # 暂时固定，测试
                init_config = sender_conf.get(f"{send_type}_init_config", {})
                cos_model_resp = each_data.get("cos_model", {})
                doc_cus_des = ""
                if cos_model_resp and skip_ads:
                    # 经过模型判断
                    if cos_model_resp["result"] == 1:
                        # 广告标记
                        doc_cus_des = f"👿广告[概率：{cos_model_resp['probability']}]"
                    else:
                        doc_cus_des = "🤓非广告"

                each_data["doc_cus_des"] = doc_cus_des
                each_data["doc_link"] = get_bak_doc_link(
                    link_source=link_source, doc_data=each_data
                )
                # 每次分发休眠一定时间
                time.sleep(delta_time)
                send_factory(
                    send_type=send_type, init_config=init_config, send_data=each_data
                )
    else:
        LOGGER.error()("未配置分发器!")


if __name__ == "__main__":
    send_config = {
        "basic_filter": {"doc_source": "liuli_wechat"},
        "sender_list": ["wecom"],
        "query_days": 5,
        "skip_ads": False,
        "delta_time": 3,
        "custom_filter": {
            "wecom": {"delta_time": 1, "ignore_doc_source_name": ["老胡的储物柜"]}
        },
    }
    send_doc(send_config)
