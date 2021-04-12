#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/12.
    Description：分发到企业微信终端
    Changelog: all notable changes to this file will be documented
"""

import json
import time

import requests

from src.config import Config
from src.sender.base import SenderBase
from src.sender.utils import send_post_request
from src.utils import LOGGER


class WeComSender(SenderBase):
    """
    企业微信分发类
    """

    def __init__(self, send_config: dict):
        """
        初始化相关变量
        :param send_config:
        """
        super().__init__(send_type="wecom", send_config=send_config)
        self.wecom_id = send_config.get("wecom_id", Config.WECOM_ID)
        self.wecom_agent_id = send_config.get("wecom_agent_id", Config.WECOM_AGENT_ID)
        self.wecom_secret = send_config.get("wecom_secret", Config.WECOM_SECRET)
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_token()}"

    def get_token(self):
        """
        获取Token
        :return:
        """
        data = {
            "corpid": self.wecom_id,
            "corpsecret": self.wecom_secret,
        }
        token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        json_data = requests.get(token_url, params=data).json()
        return json_data.get("access_token", "")

    def send_text_card(self, send_data):
        """
        发送卡片消息
        :param send_data:
        :return:
        """
        doc_name = send_data["doc_name"]
        doc_source = send_data["doc_source"]
        doc_link = send_data["doc_link"]
        doc_content = send_data["doc_content"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_source_name = send_data["doc_source_name"]
        doc_ts = send_data["doc_ts"]
        doc_date = time.strftime("%Y-%m-%d", time.localtime(doc_ts))

        doc_des_info = f"亲，来自 {doc_source} 源的 {doc_source_name} 有更新啦：{doc_content}"
        doc_des = f'<div class="black">{doc_date} | {doc_cus_des}</div>\n<div class="normal">{doc_des_info}</div>\n来自[2c]👉技术支持❤️'

        data = {
            "toparty": 1,
            "msgtype": "textcard",
            "agentid": self.wecom_agent_id,
            "textcard": {
                "title": f"[{doc_source_name}]{doc_name}",
                "description": doc_des,
                "url": doc_link,
                "btntxt": "更多",
            },
            "safe": 0,
        }

        data = json.dumps(data, ensure_ascii=False)
        try:
            resp_dict = requests.post(
                url=self.url,
                data=data.encode("utf-8").decode("latin1"),
                headers={"Content-Type": "application/json"},
            ).json()
            return resp_dict
        except Exception as e:
            resp_dict = {}
            LOGGER.error(f"请求出错：{e}")
        return resp_dict

    def send(self, send_data) -> bool:
        """
        下发到钉钉终端
        :param send_data: 下发内容字典，字段开发者自定义
        :return:
        """
        doc_name = send_data["doc_name"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_id = send_data["doc_id"]
        doc_source_name = send_data["doc_source_name"]
        is_send = self.is_send(doc_id=doc_id)
        send_status = True
        if not is_send:
            # 开始进行下发
            resp_dict = self.send_text_card(send_data=send_data)
            print(resp_dict)
            if resp_dict:
                if resp_dict.get("errcode") == 0:
                    # 下发成功
                    LOGGER.info(
                        f"[2c_{doc_source_name}]_{doc_name} {doc_cus_des}：{doc_id} 成功分发到 {self.send_type}"
                    )
                    # 将状态持久化到数据库
                    self.sl_coll.insert_one(
                        {"send_type": self.send_type, "doc_id": doc_id}
                    )
                    send_status = True
                else:
                    LOGGER.error(
                        f"[2c_{doc_source_name}]_{doc_name} {doc_cus_des}：{doc_id} 分发到 {self.send_type} 失败：{resp_dict.get('errmsg')}"
                    )
            else:
                LOGGER.error(
                    f"[2c_{doc_source_name}]_{doc_name} {doc_cus_des}：{doc_id} 分发到 {self.send_type} 失败!"
                )

        return send_status


def send(send_config: dict, send_data: dict) -> bool:
    """
    下发到钉钉终端
    :param send_config: 下发终端配置
    :param send_data: 下发内容字典，字段开发者自定义
    :return:
    """
    return WeComSender(send_config=send_config).send(send_data)


if __name__ == "__main__":
    send(
        send_config={},
        send_data={
            "doc_id": "f42460107f69c9e929f8d591243efeb2",
            "doc_content": "普通人搞一百万有多难？",
            "doc_date": "2021-04-11",
            "doc_des": "",
            "doc_ext": {},
            "doc_link": "https://mp.weixin.qq.com/s/J9Ejaw9x9fXDZ4-hsrhhtw",
            "doc_name": "普通人搞一百万有多难？",
            "doc_source": "wechat",
            "doc_source_des": "前码农&产品人，现自由职业者，创业者。",
            "doc_source_name": "stormzhang",
            "doc_cus_des": "广告",
            "doc_ts": 1618136819.0,
            "cos_model": {
                "model_name": "cos",
                "result": 0,
                "probability": 0.0,
                "feature_dict": {
                    "is_black": False,
                    "is_white": False,
                    "text": "普通人搞一百万有多难？",
                },
            },
        },
    )
