"""
    Created by howie.hu at 2023-03-27.
    Description: 更新书签，以 url 判断唯一，存在就更新，反之新增
    Changelog: all notable changes to this file will be documented
"""
import time

from flask import current_app, request
from pymongo import UpdateOne

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.databases import MongodbBase, mongodb_batch_operate, mongodb_update_data


@jwt_required()
def bm_update():
    """
    更新浏览器书签
    eg:
    {
        "url": "https://github.com/howie6879/liuli",
        "tags": ["1", "2"],
        "title": "title",
        "des": "des"
    }
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll_bm = mongodb_base.get_collection(coll_name="liuli_bm")
    coll_bm_tags = mongodb_base.get_collection(coll_name="liuli_bm_tags")
    # 获取基础数据
    post_data: dict = request.json
    url = post_data.get("url", "").strip()
    # 全部小写去空格
    tags = [str(i).lower().strip() for i in post_data.get("tags", [])]
    title = post_data.get("title", "")
    des = post_data.get("des", "")

    if url and tags:
        result = UniResponse.SUCCESS
        # 更新标签
        db_op_list = []
        for each_tag in tags:
            db_op_list.append(
                UpdateOne(
                    {"tag": each_tag},
                    {"$set": {"updated_at": int(time.time())}},
                    upsert=True,
                )
            )

        bm_tags_res = mongodb_batch_operate(
            coll_conn=coll_bm_tags, target_list=db_op_list
        )

        if not bm_tags_res["status"]:
            # 更新 Tag 失败
            result = UniResponse.DB_ERR
            err_info = f"update web bookmarket tag failed! DB response info -> {bm_tags_res['info']}"
            app_logger.error(err_info)

        else:
            bm_db_res = mongodb_update_data(
                coll_conn=coll_bm,
                filter_dict={"url": url},
                update_data={
                    "$set": {
                        "tags": tags,
                        "title": title.strip(),
                        "des": des.strip(),
                        "updated_at": int(time.time()),
                    }
                },
            )

            if not bm_db_res["status"]:
                # 更新失败
                result = UniResponse.DB_ERR
                err_info = f"update web bookmarket failed! DB response info -> {bm_db_res['info']}"
                app_logger.error(err_info)
    else:
        result = result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.BM_URL_TAG_IS_EMPTY,
            ResponseField.STATUS: ResponseCode.BM_URL_TAG_IS_EMPTY,
        }

    return response_handle(request=request, dict_value=result)
