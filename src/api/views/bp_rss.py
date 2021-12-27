"""
    Created by howie.hu at 2021-12-27.
    Description: 2C RSS 接口
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint, current_app, render_template, request

from src.databases.mongodb_base import MongodbBase
from src.databases.mongodb_tools import mongodb_find

bp_rss = Blueprint("rss", __name__, url_prefix="/rss")


@bp_rss.route("/feeds/<rss_name>", methods=["GET"], strict_slashes=False)
def feeds(rss_name):
    """
    示例接口
    :return:
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    logger = current_app.config["app_logger"]
    coll_rss_conn = mongodb_base.get_collection(coll_name="2c_rss")
    filter_dict = {"doc_source_name": rss_name}
    db_res = mongodb_find(
        coll_conn=coll_rss_conn, filter_dict=filter_dict, return_dict={}, limit=1
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
            msg = f"{rss_name} 不存在，请先录入!"
            logger.error(msg)
    else:
        # 查询失败
        msg = f"{rss_name} 查询失败!"
        logger.error(msg)

    return (
        rss_data,
        200,
        {"Content-Type": "text/xml; charset=utf-8"},
    )
