"""
    Created by howie.hu at 2023-03-26.
    Description: 删除 doc_source
    Changelog: all notable changes to this file will be documented
"""

from flask import current_app, request

from src.api.common import UniResponse, jwt_required, response_handle
from src.databases import MongodbBase, mongodb_delete_many_data


@jwt_required()
def doc_source_delete():
    """删除 doc_source
    eg:
    {
        "username": "liuli",
        "doc_source": "wechat"
    }
    Returns:
        Response: 响应类
    """
    # 获取基本配置
    mongodb_base: MongodbBase = current_app.config["mongodb_base"]
    app_logger = current_app.config["app_logger"]
    coll = mongodb_base.get_collection(coll_name="liuli_doc_source")
    # 获取基础数据
    post_data: dict = request.json
    doc_source = post_data.get("doc_source", "")
    username = post_data.get("username", "")
    result = UniResponse.SUCCESS

    db_res = mongodb_delete_many_data(
        coll_conn=coll, filter_dict={"doc_source": doc_source, "username": username}
    )

    if not db_res["status"]:
        # 删除失败
        result = UniResponse.DB_ERR
        err_info = (
            f"delete doc_source config failed! DB response info -> {db_res['info']}"
        )
        app_logger.error(err_info)

    return response_handle(request=request, dict_value=result)
