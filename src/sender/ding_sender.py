#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：分发到钉钉终端
    Changelog: all notable changes to this file will be documented
"""

import time

from src.common.remote import send_post_request
from src.config import Config
from src.sender.base import SenderBase
from src.utils import LOGGER


class DingSender(SenderBase):
    """
    钉钉分发类
    """

    def __init__(self, init_config: dict):
        """
        初始化相关变量
        :param init_config:
        """
        super().__init__(send_type="ding", init_config=init_config)
        dd_token = init_config.get("dd_token", Config.LL_DD_TOKEN)
        self.url = f"https://oapi.dingtalk.com/robot/send?access_token={dd_token}"

    def send(self, send_data) -> bool:
        """
        下发到钉钉终端
        :param send_data: 下发内容字典，字段开发者自定义
        :return:
        """
        doc_id = send_data["doc_id"]
        doc_name = send_data["doc_name"]
        doc_source = send_data["doc_source"]
        doc_link = send_data["doc_link"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_source_name = send_data["doc_source_name"]
        doc_keywords = send_data["doc_keywords"]
        is_send = self.is_send(doc_id=doc_id)
        doc_date = send_data["doc_date"]
        send_status = True
        if not is_send:
            # 开始进行下发
            # data = {
            #     "msgtype": "link",
            #     "link": {
            #         "text": f"[liuli]{doc_source_name}: {doc_cus_des}\n亲，{doc_source} 源有更新\n",
            #         "title": doc_name,
            #         "picUrl": "",
            #         "messageUrl": doc_link,
            #     },
            # }
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"## [{doc_name}]({doc_link})\n\n**{doc_source_name}** | **{doc_date}** | **{doc_cus_des}** \n\n-----\n\n> 文章关键字：{doc_keywords}\n\n-----\n\n识别错误？点击[广告反馈](https://github.com/howie6879/liuli/issues/4)  👉来自[liuli](https://github.com/howie6879/liuli)技术支持❤️",
                    "title": f"亲，{doc_source} 源有更新啦!👉{doc_name} ",
                },
            }
            resp_dict = send_post_request(
                url=self.url, data=data, headers={"Content-Type": "application/json"}
            )
            notice_msg = f"{doc_cus_des}👉{doc_source_name}_{doc_name}：{doc_link} 分发到 {self.send_type}"
            if resp_dict:
                if resp_dict.get("errmsg") == "ok":
                    # 将状态持久化到数据库
                    self.sl_coll.insert_one(
                        {
                            "send_type": self.send_type,
                            "doc_id": doc_id,
                            "ts": int(time.time()),
                        }
                    )
                    # 下发成功
                    LOGGER.info(f"{notice_msg} 成功！")
                else:
                    LOGGER.error(f"{notice_msg} 失败：{resp_dict.get('errmsg')}")
                    send_status = False
            else:
                LOGGER.error(f"{notice_msg} 失败!")
                send_status = False

        return send_status


def send(init_config: dict, send_data: dict) -> bool:
    """
    下发到钉钉终端
    :param init_config: 下发终端配置
    :param send_data: 下发内容字典，字段开发者自定义
    :return:
    """
    return DingSender(init_config=init_config).send(send_data)
