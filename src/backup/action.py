"""
    Created by howie.hu at 2022-01-21.
    Description: 执行备份动作
        - 文章备份命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/backup/action.py
        - 准备数据命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/collect_factory.py
    Changelog: all notable changes to this file will be documented
"""
import time

from copy import deepcopy

from src.backup.backup_factory import backup_factory
from src.backup.utils import get_bak_doc_html
from src.config import Config
from src.databases import MongodbManager
from src.databases.mongodb_tools import mongodb_find
from src.processor import processor_dict
from src.utils.log import LOGGER


def backup_doc(backup_config: dict):
    """对文章进行备份

    Args:
        backup_config (dict): 备份配置
    """
    backup_list = backup_config["backup_list"]
    query_days = backup_config.get("query_days", 2)
    delta_time = backup_config.get("delta_time", 3)
    basic_filter = backup_config.get("basic_filter", {})
    doc_html_dict = backup_config.get("doc_html_dict", {})
    init_config = backup_config.get("init_config", {})
    after_get_content = backup_config.get("after_get_content", [])
    if backup_list:
        mongo_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        coll = mongo_base.get_collection(coll_name="liuli_articles")
        cur_ts = int(time.time())
        filter_dict = {
            **basic_filter,
            **{
                # 时间范围，除第一次外后面其实可以去掉
                "doc_ts": {"$gte": cur_ts - (query_days * 24 * 60 * 60), "$lte": cur_ts}
            },
        }
        db_res = mongodb_find(
            coll_conn=coll,
            filter_dict=filter_dict,
            return_dict={
                "_id": 0,
                "doc_source": 1,
                "doc_source_name": 1,
                "doc_core_html": 1,
                "doc_html": 1,
                "doc_name": 1,
                "doc_link": 1,
            },
        )

        if db_res["status"]:
            # 查找所有可备份文章
            for each_data in db_res["info"]:
                for each in backup_list:
                    # 每次备份休眠一定时间
                    time.sleep(delta_time)
                    backup_ins = backup_factory(
                        backup_type=each, init_config=init_config
                    )
                    # 获取文档源
                    doc_source = each_data["doc_source"]
                    # 获取最终存储数据
                    doc_html = get_bak_doc_html(
                        doc_data=each_data,
                        doc_html_type=doc_html_dict.get(doc_source, "default"),
                    )
                    # 执行获取文本后的钩子函数
                    for func_dict in after_get_content:
                        cur_func_dict = deepcopy(func_dict)
                        func_name = cur_func_dict.pop("func")
                        LOGGER.info(
                            f"处理器(backup:after_get_content): {func_name} 正在执行..."
                        )
                        cur_func_dict.update({"text": doc_html})
                        doc_html = processor_dict[func_name](**cur_func_dict)
                    # 进行保存动作
                    each_data["doc_html"] = doc_html
                    backup_ins.save(each_data)
            LOGGER.info(f"Backup 执行成功，备份文章 {len(db_res['info'])} 篇")
        else:
            LOGGER.error(f"Backup 数据查询失败! {db_res['info']}")
    else:
        LOGGER.error("Backup 未配置备份源!")


if __name__ == "__main__":
    b_backup = {
        "backup_list": ["github", "mongodb"],
        # "backup_list": ["mongodb"],
        "query_days": 3,
        "delta_time": 3,
        "basic_filter": {"doc_source": "liuli_book"},
        "doc_html_dict": {"liuli_book": "book"},
        "init_config": {},
        "after_get_content": [],
    }
    w_backup = {
        "backup_list": ["github", "mongodb"],
        "query_days": 3,
        "delta_time": 3,
        "init_config": {},
        "basic_filter": {"doc_source": "liuli_wechat"},
        "after_get_content": [
            {
                "func": "str_replace",
                "before_str": 'data-src="',
                "after_str": 'src="https://images.weserv.nl/?url=',
            }
        ],
    }
    backup_doc(w_backup)
