#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：配置文件
    Changelog: all notable changes to this file will be documented
"""

import os


class Config:
    """
    配置类
    """

    # 基础配置
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "model_data")

    # Flask API配置
    DEBUG = True if os.getenv("CC_FLASK_DEBUG", "0") == "1" else False
    TIMEZONE = "Asia/Shanghai"
    HOST = os.getenv("CC_HOST", "127.0.0.1")
    HTTP_PORT = os.getenv("CC_HTTP_PORT", 8060)
    WORKERS = os.getenv("CC_WORKERS", 1)
    AUTH_KEY = os.getenv("CC_AUTH_KEY", "123456")

    # 数据库配置
    MONGODB_CONFIG = {
        # "mongodb://0.0.0.0:27017"
        "username": os.getenv("CC_M_USER", ""),
        "password": os.getenv("CC_M_PASS", ""),
        "host": os.getenv("CC_M_HOST", "0.0.0.0"),
        "port": int(os.getenv("CC_M_PORT", "27017")),
        "db": os.getenv("CC_M_DB", "2c"),
    }

    # 分发配置，目标支持：ding[钉钉]、wecom[企业微信]、tg[Telegram] 等等
    # 目前仅支持钉钉
    SENDER_LIST = ["ding"]
    # 钉钉 URL，如果 SENDER_LIST 包含 ding ，CC_D_TOKEN 配置就必须填写
    # 申请钉钉TOKEN时候，关键字必须带有 [2c]
    DD_URL = f"https://oapi.dingtalk.com/robot/send?access_token={os.getenv('CC_D_TOKEN', '')}"

    # 订阅的公众号配置
    WECHAT_LIST = [
        "小道消息",
        "是不是很酷",
        "caoz的梦呓",
        "美团技术团队",
        "阿里技术",
        "ThoughtWorks洞见",
        "小米技术",
        "老胡的储物柜",
        "我就BB怎么了",
        "stormzhang",
    ]


if __name__ == "__main__":
    print(Config.RSS_DICT.keys())
