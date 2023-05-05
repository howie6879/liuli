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
from src.utils import LOGGER


class WeComSender(SenderBase):
    """
    企业微信分发类
    """

    def __init__(self, init_config: dict):
        """
        初始化相关变量
        :param init_config:
        """
        super().__init__(send_type="wecom", init_config=init_config)
        self.wecom_id = init_config.get("wecom_id", Config.LL_WECOM_ID)
        self.wecom_agent_id = init_config.get(
            "wecom_agent_id", Config.LL_WECOM_AGENT_ID
        )
        self.wecom_secret = init_config.get("wecom_secret", Config.LL_WECOM_SECRET)
        self.access_token = self.get_token()
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        self.wecom_party_list = init_config.get(
            "wecom_party_list", Config.LL_WECOM_PARTY
        )
        self.wecom_to_user = init_config.get("wecom_to_user", Config.LL_WECOM_TO_USER)
        self.wecom_party = ""
        # 如果部门和用户都没有，则默认发送给所有人
        if not self.wecom_party_list and not self.wecom_to_user:
            self.wecom_to_user = "@all"
        # 其他情况，则按用户填写的发送(既发用户，也发部门)
        else:
            self.change_wecom_party_to_id()

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
        json_data = requests.get(token_url, params=data, timeout=10).json()
        return json_data.get("access_token", "")

    def get_party(self):
        """
        获取部门列表
        :return:
        """
        data = {
            "access_token": self.access_token,
        }
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/list"
        json_data = requests.get(url, params=data, timeout=10).json()
        return json_data.get("department", [])

    def change_wecom_party_to_id(self):
        """
        将部门名称转换为部门ID
        :return:
        """
        party_list = self.get_party()
        party_ids = [
            party_info["id"]
            for party_info in party_list
            if party_info["name"] in self.wecom_party_list
        ]
        for party_id in party_ids:
            self.wecom_party += f"{party_id}|"
        self.wecom_party = self.wecom_party[:-1]

    def send_text_card(self, send_data):
        """
        发送卡片消息
        :param send_data:
        :return:
        """
        doc_name = send_data["doc_name"]
        doc_source = send_data["doc_source"]
        doc_link = send_data["doc_link"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_source_name = send_data["doc_source_name"]
        doc_keywords = send_data["doc_keywords"]
        doc_ts = send_data["doc_ts"]
        doc_date = send_data["doc_date"] or time.strftime(
            "%Y-%m-%d: %H:%M:%S", time.localtime(doc_ts)
        )

        doc_des_info = f"亲，来自 {doc_source} 源的 {doc_source_name} 有更新啦!"
        if doc_keywords:
            doc_des_info += f"\n\n文章关键字：{doc_keywords}"

        doc_des_head = f"{doc_date} | {doc_cus_des}" if doc_cus_des else f"{doc_date}"
        doc_des = f'<div class="black">{doc_des_head}</div>\n<div class="normal">{doc_des_info}</div>\n来自[liuli]👉技术支持❤️'

        data = {
            "touser": self.wecom_to_user,
            "toparty": self.wecom_party,
            "msgtype": "textcard",
            "agentid": self.wecom_agent_id,
            "textcard": {
                "title": f"[{doc_source_name}] {doc_name}",
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
                timeout=10,
            ).json()
            return resp_dict
        except Exception as e:
            resp_dict = {}
            LOGGER.error(f"请求出错：{e}")
        return resp_dict

    def send(self, send_data) -> bool:
        """
        下发到微信终端
        :param send_data: 下发内容字典，字段开发者自定义
        :return:
        """
        doc_name = send_data["doc_name"]
        doc_cus_des = send_data["doc_cus_des"]
        doc_id = send_data["doc_id"]
        doc_link = send_data["doc_link"]
        doc_source_name = send_data["doc_source_name"]
        is_send = self.is_send(doc_id=doc_id)
        send_status = True
        if not is_send:
            # 开始进行下发
            resp_dict = self.send_text_card(send_data=send_data)
            notice_msg = f"{doc_cus_des}👉{doc_source_name}_{doc_name}：{doc_link} 分发到 {self.send_type}"
            if resp_dict:
                if resp_dict.get("errcode") == 0:
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
                    send_status = False
                    LOGGER.error(f"{notice_msg} 失败：{resp_dict.get('errmsg')}")
            else:
                send_status = False
                LOGGER.error(f"{notice_msg} 失败!")

        return send_status


def send(init_config: dict, send_data: dict) -> bool:
    """
    下发到终端
    :param init_config: 下发终端配置
    :param send_data: 下发内容字典，字段开发者自定义
    :return:
    """
    return WeComSender(init_config=init_config).send(send_data)


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
