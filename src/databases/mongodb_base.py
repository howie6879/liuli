#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：MongoDB 连接类
    Changelog: all notable changes to this file will be documented
"""

from pymongo import MongoClient

from src.utils.tools import md5_encryption


class MongodbBase:
    """
    Mongodb连接类
    """

    _db = {}
    _collection = {}

    def __init__(self, mongodb_config: dict):
        self.mongodb_config = mongodb_config
        self.mongodb_uri = "mongodb://{account}{host}:{port}/{db}".format(
            account="{username}:{password}@".format(
                username=self.mongodb_config["username"],
                password=self.mongodb_config["password"],
            )
            if self.mongodb_config.get("username")
            else "",
            host=self.mongodb_config.get("host", "localhost"),
            port=self.mongodb_config.get("port", 271017),
            db=self.mongodb_config.get("db", "2c"),
        )
        self.client = MongoClient(self.mongodb_uri)

    def get_db(self, db_name: str = ""):
        """
        获取数据库实例
        :param db_name: 数据名称
        :return:
        """

        if not db_name:
            db_name = self.mongodb_config["db"]
        if db_name not in self._db:
            self._db[db_name] = self.client[db_name]

        return self._db[db_name]

    def get_collection(self, coll_name, db_name: str = ""):
        """
        获取集合
        :param coll_name: 集合名称
        :param db_name: 数据库名称
        :return:
        """
        if not db_name:
            db_name = self.mongodb_config["db"]
        coll_key = db_name + coll_name
        if coll_key not in self._collection:
            self._collection[coll_key] = self.get_db(db_name)[coll_name]

        return self._collection[coll_key]


class MongodbManager:
    """
    Mongodb管理类，提供单例连接类
    """

    _mongodb_dict = {}

    @classmethod
    def get_mongo_base(cls, mongodb_config: dict) -> MongodbBase:
        """
        MongoDB连接类
        """
        key = md5_encryption(f"{mongodb_config}")
        if key not in cls._mongodb_dict:
            cls._mongodb_dict[key] = MongodbBase(mongodb_config)

        return cls._mongodb_dict[key]


if __name__ == "__main__":
    from src.config import Config

    mongo_base = MongodbManager.get_mongo_base(Config.MONGODB_CONFIG)
    print(mongo_base.mongodb_uri)
