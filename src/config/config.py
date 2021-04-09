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

    MONGODB_CONFIG = {
        # "mongodb://0.0.0.0:27017"
        "username": os.getenv("CC_M_USER", ""),
        "password": os.getenv("CC_M_PASS", ""),
        "host": os.getenv("CC_M_HOST", "0.0.0.0"),
        "port": int(os.getenv("CC_M_PORT", "27017")),
        "db": os.getenv("CC_M_DB", "2c"),
    }
    DD_URL = f"https://oapi.dingtalk.com/robot/send?access_token={os.getenv('CC_D_TOKEN', '')}"
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "model_data")

    # 关注的公众号
    WECHAT_LIST = [
        "是不是很酷",
        "caoz的梦呓",
        "美团技术团队",
        "阿里技术",
        "ThoughtWorks洞见",
        "小米技术",
        "老胡的储物柜",
    ]

    # 微信公众号订阅源，依赖项目：https://github.com/hellodword/wechat-feeds
    RSS_DICT = {
        "是不是很酷": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzU4NTIxODYwMQ==.xml",
        "caoz的梦呓": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzI0MjA1Mjg2Ng==.xml",
        "美团技术团队": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MjM5NjQ5MTI5OA==.xml",
        "阿里技术": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzIzOTU0NTQ0MA==.xml",
        "ThoughtWorks洞见": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MjM5MjY3OTgwMA==.xml",
        "小米技术": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzUxMDQxMDMyNg==.xml",
        "老胡的储物柜": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzU4MTA0NDQ0Ng==.xml",
        "小道消息": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MjM5ODIyMTE0MA==.xml",
        "我就BB怎么了": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzA5ODg5NDk1Ng==.xml",
        "路人甲TM": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzIzMDQyMjcxOA==.xml",
        "stormzhang": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzA4NTQwNDcyMA==.xml",
        "findyi": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzA3MzA5MTU4NA==.xml",
    }


if __name__ == "__main__":
    print(Config.BASE_DIR)
