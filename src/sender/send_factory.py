# !/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：分发器工厂，支持分发终端如下：
        - 钉钉
    Changelog: all notable changes to this file will be documented
"""

from importlib import import_module

from src.utils import LOGGER


def send_factory(send_type: str, send_config: dict, send_data: dict) -> bool:
    """
    分发器工厂函数
    :param send_type: 下发终端类型
    :param send_config: 下发终端配置
    :param send_data: 下发内容字典，字段开发者自定义
    :return:
    """
    send_status = False
    try:
        send_module = import_module(f"src.sender.{send_type}_sender")
        send_status = send_module.send(send_config, send_data)
    except ModuleNotFoundError:
        LOGGER.error(f"目标终端类型不存在 {send_type} - {send_config} - {send_data}")
    return send_status


if __name__ == "__main__":
    send_config = {
        "url": "https://oapi.dingtalk.com/robot/send?access_token=dca91d0f3ea019ef92f8f8c347dddfe9514e682d107afb8163879608743453df"
    }
    send_data = {
        "doc_id": "aabf6b7984424372ee5232b2d83037cb",
        "doc_content": "数字化时代再提业务平台化",
        "doc_date": "2021-04-09",
        "doc_cus_des": "非广告",
        "doc_ext": {},
        "doc_link": "https://mp.weixin.qq.com/s/ubrsOCTu1KPLtHu4e9LFlw",
        "doc_name": "数字化时代再提业务平台化",
        "doc_source": "wechat",
        "doc_source_des": "最新技术雷达/各类技术干货/精选职位招聘/精彩活动预告/经典案例故事，就在ThoughtWorks。",
        "doc_source_name": "ThoughtWorks洞见",
        "doc_ts": 1617960250.0,
    }
    send_factory(send_type="ding", send_config=send_config, send_data=send_data)
