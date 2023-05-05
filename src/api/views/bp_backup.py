"""
    Created by howie.hu at 2021-12-27.
    Description: liuli backup html 接口
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint, current_app

from src.databases.mongodb_base import MongodbBase
from src.databases.mongodb_tools import mongodb_find
from src.utils.tools import text_decompress

bp_backup = Blueprint("backup", __name__, url_prefix="/backup")


@bp_backup.route(
    "/<doc_source>/<doc_source_name>/<doc_name>",
    methods=["GET"],
    strict_slashes=False,
)
def backup(doc_source, doc_source_name, doc_name):
    """备份文章获取接口
    http://127.0.0.1:8765/backup/liuli_wechat/老胡的周刊（第089期）
    Args:
        doc_source ([type]): 文章来源
        doc_source_name ([type]): 文章来源作者
        doc_name ([type]): 文章名称

    Returns:
        [type]: Flask Response
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    logger = current_app.config["app_logger"]

    # 获取变量
    file_path = f"{doc_source}/{doc_source_name}/{doc_name}"
    coll_conn = mongodb_base.get_collection(coll_name="liuli_backup")
    filter_dict = {
        "doc_source": doc_source,
        "doc_source_name": doc_source_name,
        "doc_name": doc_name,
    }
    db_res = mongodb_find(
        coll_conn=coll_conn,
        filter_dict=filter_dict,
        return_dict={"_id": 0},
        limit=1,
    )
    db_satus, db_info = db_res["status"], db_res["info"]
    content = ""
    if db_satus:
        # 查询成功
        if db_info:
            # 存在
            content = db_info[0]["content"]
        else:
            # 不存在 rss
            content = f"文章 {file_path} 不存在，请先进行备份!"
            logger.error(content)
    else:
        # 查询失败
        content = f"{file_path} 查询失败!"
        logger.error(content)

    return (
        text_decompress(content),
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )
