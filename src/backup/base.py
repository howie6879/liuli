"""
    Created by howie.hu at 2022-01-15.
    Description: 备份工厂父类
    Changelog: all notable changes to this file will be documented
"""

import time

from src.config import Config
from src.databases import MongodbBase, MongodbManager
from src.utils import LOGGER


class BackupBase:
    """
    备份工厂父类
    :return:
    """

    def __init__(self, backup_type: str, init_config: dict):
        """
        初始化相关配置
        :param backup_type: 下发目标类型
        :param init_config: 下发目标类型相关配置，如密钥之类
        """
        self.backup_type = backup_type
        self.init_config = init_config
        # 初始化数据库
        self.mongo_base: MongodbBase = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        # liuli_send_list 存储所有已经备份过的文章列表
        self.bak_coll = self.mongo_base.get_collection(coll_name="liuli_backup_list")

    def is_backup(self, doc_source: str, doc_source_name: str, doc_name: str) -> bool:
        """保存文件备份状态

        Args:
            doc_source (str): 文章获取源
            doc_source_name (str): 文章源
            doc_name (str): 文章名字
        Returns:
            bool: 是否成功
        """
        curl = self.bak_coll.find(
            {
                "backup_type": self.backup_type,
                "doc_source": doc_source,
                "doc_source_name": doc_source_name,
                "doc_name": doc_name,
            }
        )
        return True if list(curl) else False

    def save_backup(self, doc_source: str, doc_source_name: str, doc_name: str) -> bool:
        """保存文件备份状态

        Args:
            doc_source (str): 文章获取源
            doc_source_name (str): 文章源
            doc_name (str): 文章名字
        Returns:
            bool: 是否成功
        """
        file_msg = f"{doc_source}/{doc_source_name}/{doc_name}"
        try:
            filter_dict = {
                "backup_type": self.backup_type,
                "doc_source": doc_source,
                "doc_source_name": doc_source_name,
                "doc_name": doc_name,
            }
            update_data = {"$set": {**filter_dict, **{"ts": int(time.time())}}}
            self.bak_coll.update_one(
                filter=filter_dict, update=update_data, upsert=True
            )
            LOGGER.info(f"Backup({self.backup_type}): 文章 {file_msg} 状态保存成功！")
        except Exception as e:
            LOGGER.error(f"Backup({self.backup_type}): 文章 {file_msg} 状态保存失败！{e}")

    def delete_backup(
        self, doc_source: str, doc_source_name: str, doc_name: str
    ) -> bool:
        """删除文件分备份状态

        Args:
            doc_source (str): 文章获取源
            doc_source_name (str): 文章源
            doc_name (str): 文章名字
        Returns:
            bool: 是否成功
        """
        file_msg = f"{doc_source}/{doc_source_name}/{doc_name}"
        try:
            self.bak_coll.delete_one(
                {
                    "backup_type": self.backup_type,
                    "doc_source": doc_source,
                    "doc_source_name": doc_source_name,
                    "doc_name": doc_name,
                }
            )
            LOGGER.info(f"Backup({self.backup_type}): 文章 {file_msg} 状态删除成功！")
        except Exception as e:
            LOGGER.error(f"Backup({self.backup_type}): 文章 {file_msg} 状态删除失败！{e}")

    def save(self, backup_data) -> bool:
        """
        执行备份动作，每个子类必须实现的方法
        :param send_data: 发送列表
        :return:
        """
        raise NotImplementedError
