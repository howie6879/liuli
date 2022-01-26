"""
    Created by howie.hu at 2021-12-27.
    Description: RSS相关脚本
        - 生成RSS命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/processor/rss/doc2rss.py
    Changelog: all notable changes to this file will be documented
"""
import time

from datetime import datetime

import pytz

from feedgen.feed import FeedGenerator

from src.common.db_utils import get_doc_source_name_dict
from src.config import Config
from src.databases.mongodb_base import MongodbManager
from src.databases.mongodb_tools import mongodb_find, mongodb_update_data
from src.processor.rss.utils import get_rss_doc_link
from src.utils import LOGGER


def to_rss(doc_source_list: list = None, link_source: str = "self"):
    """为文章生成RSS

    Args:
        doc_source_list (list, optional): 文章来源列表. Defaults to None.
        link_source (str, optional): 链接返回规则类型，基于备份器，目前支持字段如下:
            - self: 不替换，用本身的 doc_link
            - mongodb: 用 liuli api 服务的连接 {LL_DOMAIN}/backup/{doc_source}/{doc_source_name}/{doc_name}
            - github: 用 github 仓库地址 {LL_GITHUB_DOMAIN}/{doc_source}/{doc_source_name}/{doc_name}.html
    """
    # 获取 doc_source 下的 doc_source_name 组成的字典
    doc_source_name_dict: dict = get_doc_source_name_dict(doc_source_list)
    # 数据库初始化
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll_articles_conn = mongo_base.get_collection(
        coll_name="liuli_articles", db_name="liuli"
    )
    coll_rss_conn = mongo_base.get_collection(coll_name="liuli_rss", db_name="liuli")
    for doc_source, doc_source_name_list in doc_source_name_dict.items():
        for doc_source_name in doc_source_name_list:
            filter_dict = {"doc_source_name": doc_source_name, "doc_source": doc_source}
            return_dict = {
                "doc_source_name": 1,
                "doc_source": 1,
                "doc_name": 1,
                "doc_des": 1,
                "doc_link": 1,
                "doc_core_html": 1,
                "doc_author": 1,
                "doc_date": 1,
                "doc_ts": 1,
            }
            # 提取文章
            f_db_res = mongodb_find(
                coll_conn=coll_articles_conn,
                filter_dict=filter_dict,
                return_dict=return_dict,
                sorted_key="doc_ts",
                # 倒序
                sorted_index=1,
                # 最近10篇文章
                limit=10,
            )
            f_db_satus, f_db_info = f_db_res["status"], f_db_res["info"]
            if f_db_satus:
                if f_db_info:
                    # 查询成功且有数据
                    fg = FeedGenerator()
                    fg.id(doc_source_name)
                    fg.title(doc_source_name)
                    fg.author({"name": "liuli"})
                    for each in f_db_info:
                        doc_name = each["doc_name"]
                        if not doc_name:
                            continue
                        doc_des = each["doc_des"]
                        doc_link = get_rss_doc_link(
                            link_source=link_source, doc_data=each
                        )
                        doc_author = each["doc_author"] or "liuli_defaults"
                        doc_ts = each["doc_ts"]
                        # doc_core_html = each.get("doc_core_html", "")
                        # 构造 RSS
                        fe = fg.add_entry()
                        article_id = f"{doc_source} - {doc_source_name} - {doc_name}"
                        fe.id(article_id)
                        fe.title(doc_name)
                        fe.link(href=doc_link)
                        fe.description(doc_des)
                        fe.author(name=f"{article_id} - {doc_author}")
                        # 内容先为空
                        fe.content("")
                        fe.pubDate(
                            pytz.timezone("Asia/Shanghai").localize(
                                datetime.fromtimestamp(doc_ts)
                            )
                        )
                    try:
                        rss_data = str(fg.atom_str(pretty=True), "utf-8")
                        # 更新 RSS 内容
                        rss_db_data = {
                            "doc_source": doc_source,
                            "doc_source_name": doc_source_name,
                            "rss_data": rss_data,
                            "updated_at": int(time.time()),
                        }
                        rss_db_res = mongodb_update_data(
                            coll_conn=coll_rss_conn,
                            filter_dict=filter_dict,
                            update_data={"$set": rss_db_data},
                        )
                        if rss_db_res["status"]:
                            msg = f"😀 为{doc_source}: {doc_source_name} 的 {len(f_db_info)} 篇文章生成RSS成功!"
                        else:
                            msg = f"😿 为{doc_source}: {doc_source_name} 的 {len(f_db_info)} 篇文章生成RSS失败!"
                    except Exception as e:
                        msg = f"😿 为{doc_source}: {doc_source_name} 的 {len(f_db_info)} 篇文章生成RSS失败, 非法数据! {e}"

                else:
                    msg = f"查询成功 {doc_source}: {doc_source_name} 暂无历史文章!"
                LOGGER.info(msg)
            else:
                # 查询失败
                LOGGER.error(f"{doc_source}: {doc_source_name} 历史文章查询失败!")


if __name__ == "__main__":
    to_rss()
