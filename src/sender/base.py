#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：分发器父类
    Changelog: all notable changes to this file will be documented
"""
from src.config import Config
from src.databases import MongodbManager


class SenderBase:
    """
    分发器父类
    :return:
    """

    def __init__(self, send_type: str, init_config: dict):
        """
        初始化相关配置
        :param send_type: 下发目标类型
        :param init_config: 下发目标类型相关配置，如密钥之类
        """
        self.send_type = send_type
        self.init_config = init_config
        # 初始化数据库
        self.mongo_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        # liuli_send_list 存储所有已经下发过的文章列表，可以当做缓存表
        self.sl_coll = self.mongo_base.get_collection(coll_name="liuli_send_list")

    def is_send(self, doc_id: str) -> bool:
        """
        判断文章是在此类型下发过
        :param doc_id:
        :return:
        """
        curl = self.sl_coll.find({"doc_id": doc_id, "send_type": self.send_type})
        return True if list(curl) else False

    def send(self, send_data) -> bool:
        """
        执行下发动作，每个子类必须实现的方法
        :param send_data: 发送列表
        :return:
        """
        raise NotImplementedError
