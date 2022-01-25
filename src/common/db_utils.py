"""
    Created by howie.hu at 2022-01-25.
    Description: 常用的DB业务操作函数
    执行: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/common/db_utils.py
    Changelog: all notable changes to this file will be documented
"""
from src.config import Config
from src.databases.mongodb_base import MongodbManager
from src.utils.log import LOGGER

MONGO_BASE = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)


def get_doc_source_list() -> list:
    """
    从 liuli_articles 获取所有 doc_source 组成的列表
    """
    coll_conn = MONGO_BASE.get_collection(coll_name="liuli_articles")
    return coll_conn.distinct("doc_source") or []


def get_doc_source_name_dict(doc_source_list: list = None) -> dict:
    """获取 doc_source 下的 doc_source_name 组成的字典

    Args:
        doc_source_list (list, optional): [description]. Defaults to [].

    Returns:
        dict: doc_source_name 字典
    """
    doc_source_list = doc_source_list or get_doc_source_list()
    doc_source_name_dict = {}
    if doc_source_list:
        coll_conn = MONGO_BASE.get_collection(coll_name="liuli_articles")
        for doc_source in doc_source_list:
            each_res = coll_conn.distinct("doc_source_name", {"doc_source": doc_source})
            doc_source_name_dict[doc_source] = each_res
    return doc_source_name_dict


if __name__ == "__main__":
    res = get_doc_source_name_dict()
    print(res)
