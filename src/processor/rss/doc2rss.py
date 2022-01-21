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

from src import config
from src.config import Config
from src.databases.mongodb_base import MongodbManager
from src.databases.mongodb_tools import mongodb_find, mongodb_update_data
from src.utils import LOGGER


def to_rss(wechat_list: list = None):
    """为文章生成RSS

    Args:
        wechat_list (list, optional): 文章列表.
    """
    wechat_list = wechat_list or Config.WECHAT_LIST
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll_articles_conn = mongo_base.get_collection(
        coll_name="liuli_articles", db_name="liuli"
    )
    coll_rss_conn = mongo_base.get_collection(coll_name="liuli_rss", db_name="liuli")
    for wechat_name in wechat_list:
        filter_dict = {"doc_source_name": wechat_name}
        return_dict = {
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
                fg.id(wechat_name)
                fg.title(wechat_name)
                fg.author({"name": "liuli"})
                for each in f_db_info:
                    doc_name = each["doc_name"]
                    if not doc_name:
                        continue
                    doc_des = each["doc_des"]
                    doc_link = each["doc_link"]
                    doc_author = each["doc_author"] or "liuli_defaults"
                    doc_ts = each["doc_ts"]
                    doc_core_html = each.get("doc_core_html", "")
                    # 构造 RSS
                    fe = fg.add_entry()
                    fe.id(f"{wechat_name} - {doc_name}")
                    fe.title(doc_name)
                    fe.link(href=doc_link)
                    fe.description(doc_des)
                    fe.author(name=f"{wechat_name} - {doc_author}")
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
                        "doc_source_name": wechat_name,
                        "rss_data": rss_data,
                        "updated_at": int(time.time()),
                    }
                    rss_db_res = mongodb_update_data(
                        coll_conn=coll_rss_conn,
                        filter_dict=filter_dict,
                        update_data={"$set": rss_db_data},
                    )
                    if rss_db_res["status"]:
                        msg = f"😀 为 {wechat_name} 的 {len(f_db_info)} 篇文章生成RSS成功!"
                    else:
                        msg = f"😿 为 {wechat_name} 的 {len(f_db_info)} 篇文章生成RSS失败!"
                except Exception as e:
                    msg = f"😿 为 {wechat_name} 的 {len(f_db_info)} 篇文章生成RSS失败, 非法数据! {e}"

            else:
                msg = f"查询成功 {wechat_name} 暂无历史文章!"
            LOGGER.info(msg)
        else:
            # 查询失败
            LOGGER.error(f"{wechat_name} 历史文章查询失败!")


if __name__ == "__main__":
    to_rss()
