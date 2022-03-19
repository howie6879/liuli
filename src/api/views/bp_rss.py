"""
    Created by howie.hu at 2021-12-27.
    Description: liuli RSS 接口
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint, current_app

from src.databases.mongodb_base import MongodbBase
from src.databases.mongodb_tools import mongodb_find

bp_rss = Blueprint("rss", __name__, url_prefix="/rss")


@bp_rss.route("/<doc_source>/<doc_source_name>/", methods=["GET"], strict_slashes=False)
def rss(doc_source, doc_source_name):
    """RSS文章获取接口
    http://127.0.0.1:8765/rss/liuli_wechat/老胡的储物柜/
    Args:
        doc_source ([type]): 文章来源
        doc_source_name ([type]): 文章来源作者

    Returns:
        [type]: Flask Response
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    logger = current_app.config["app_logger"]

    # 获取变量
    file_path = f"{doc_source}/{doc_source_name}"
    coll_conn = mongodb_base.get_collection(coll_name="liuli_rss")
    filter_dict = {
        "doc_source": doc_source,
        "doc_source_name": doc_source_name,
    }
    db_res = mongodb_find(
        coll_conn=coll_conn, filter_dict=filter_dict, return_dict={"_id": 0}, limit=1
    )
    db_satus, db_info = db_res["status"], db_res["info"]
    rss_data = ""
    if db_satus:
        # 查询成功
        if db_info:
            # 存在
            rss_data = db_info[0]["rss_data"]
        else:
            # 不存在 rss
            msg = f"{file_path} 不存在，请先录入!"
            logger.error(msg)
    else:
        # 查询失败
        msg = f"{file_path} 查询失败!"
        logger.error(msg)

    return (
        rss_data,
        200,
        {"Content-Type": "text/xml; charset=utf-8"},
    )
