#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：MongoDB 连接类
    Changelog: all notable changes to this file will be documented
"""
from urllib import parse

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
                username=parse.quote_plus(self.mongodb_config["username"]),
                password=parse.quote_plus(self.mongodb_config["password"]),
            )
            if self.mongodb_config.get("username")
            else "",
            host=self.mongodb_config.get("host", "localhost"),
            port=self.mongodb_config.get("port", 271017),
            db=self.mongodb_config.get("db", "liuli"),
        )
        self.op_db = self.mongodb_config.get("op_db", "liuli")
        self.client = MongoClient(self.mongodb_uri, connect=False)

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
        db_name = db_name or self.op_db
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
    import time

    from src.config import Config

    mongo_base = MongodbManager.get_mongo_base(Config.LL_MONGODB_CONFIG)
    coll_conn = mongo_base.get_collection(coll_name="liuli_user")

    coll_conn.update_one(
        filter={"username": "liuli"},
        update={
            "$set": {
                "username": "liuli",
                "password": md5_encryption("liuli"),
                "updated_at": int(time.time()),
            }
        },
        upsert=True,
    )
