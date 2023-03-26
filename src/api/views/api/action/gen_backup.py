"""
    Created by howie.hu at 2023-03-26.
    Description: 对数据源进行备份
    Changelog: all notable changes to this file will be documented
"""


from flask import current_app, request

from src.api.common import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    jwt_required,
    response_handle,
)
from src.backup.action import backup_doc


@jwt_required()
def action_gen_backup():
    """对数据源进行备份
    eg:
    {
        "username": "liuli",
        "doc_source": "liuli_wechat_sg",
        "doc_source_name": "老胡的储物柜"
    }
    Returns:
        Response: 响应类
    """
    # TODO 重构，基于 liuli_doc_source 读取数据
    app_logger = current_app.config["app_logger"]
    # 获取基础数据
    post_data: dict = request.json
    del post_data["username"]
    result = UniResponse.SUCCESS
    try:
        backup_doc(post_data)
    except Exception as e:
        result = {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: ResponseReply.GEN_BACKUP_FAILED,
            ResponseField.STATUS: ResponseCode.GEN_BACKUP_FAILED,
        }
        err_info = f"gen backup failed! response info -> {e}"
        app_logger.error(err_info)
    return response_handle(request=request, dict_value=result)
