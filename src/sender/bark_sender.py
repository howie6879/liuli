#!/usr/bin/env python
"""
    Created by Leslie Leung at 2021/12/28.
    Description：分发到 Bark 终端
    Changelog: all notable changes to this file will be documented
"""
import json
import time

import requests

from src.config import Config
from src.sender.base import SenderBase
from src.utils import LOGGER


class BarkSender(SenderBase):
    """
    Bark分发类
    """

    def __init__(self, init_config: dict):
        super(BarkSender, self).__init__(send_type="bark", init_config=init_config)
        bark_url = init_config.get("bark_url", Config.LL_BARK_URL)
        self.url = bark_url[:-1] if bark_url.endswith("/") else bark_url

    def send(self, send_data) -> bool:
        """
        下发到Bark终端
        :param send_data: 下发内容字典，字段开发者自定义
        :return:
        """
        doc_name = send_data["doc_name"]
        # doc_source = send_data["doc_source"]
        doc_link = send_data["doc_link"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_source_name = send_data["doc_source_name"]
        doc_id = send_data["doc_id"]
        is_send = self.is_send(doc_id=doc_id)
        send_status = True
        notice_msg = f"{doc_cus_des}👉{doc_source_name}_{doc_name}：{doc_link} 分发到 {self.send_type}"
        if not is_send:
            url = self.compose(send_data)
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if resp.status_code == 200 and json.loads(resp.text)["code"] == 200:
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
                errmsg = json.loads(resp.text)["code"]
                LOGGER.error(f"{notice_msg} 失败：{errmsg}")
                send_status = False
        return send_status

    def compose(self, send_data) -> str:
        """
        根据发送数据产生Bark请求url
        :param send_data: 下发内容字典，字段开发者自定义
        :return:
        """
        doc_name = send_data["doc_name"]
        doc_source = send_data["doc_source"]
        doc_link = send_data["doc_link"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_source_name = send_data["doc_source_name"]
        doc_keywords = send_data["doc_keywords"]
        doc_date = send_data["doc_date"]
        title = f"[{doc_source_name}]{doc_name}".replace("/", "")
        body = f"{doc_date} | {doc_cus_des}\n亲，来自 {doc_source} 源的 {doc_source_name} 有更新啦! \n\n文章关键字：{doc_keywords}\n来自[2c]👉技术支持❤"
        copy = f"?copy={doc_link}"
        return f"{self.url}/{title}/{body}{copy}"


def send(init_config: dict, send_data: dict) -> bool:
    """
    下方到Bark终端
    :param init_config: 下发终端配置
    :param send_data: 下发内容字典，字段开发者自定义
    :return:
    """
    return BarkSender(init_config=init_config).send(send_data)


if __name__ == "__main__":
    send(
        init_config={
            "wecom_id": "",
            "wecom_agent_id": 0,
            "wecom_secret": "",
            "wecom_party_list": [],
            "wecom_to_user": "",
        },
        send_data={
            "doc_id": "f42460107f69c9e929f8d591243efeb2",
            "doc_date": "2021-04-11",
            "doc_des": "",
            "doc_ext": {},
            "doc_link": "https://mp.weixin.qq.com/s/J9Ejaw9x9fXDZ4-hsrhhtw",
            "doc_name": "普通人搞一百万有多难？",
            "doc_source": "wechat",
            "doc_source_des": "前码农&产品人，现自由职业者，创业者。",
            "doc_source_name": "stormzhang",
            "doc_cus_des": "广告",
            "doc_keywords": [],
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
