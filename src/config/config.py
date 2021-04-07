#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：配置文件
    Changelog: all notable changes to this file will be documented
"""


class Config:
    """
    配置类
    """

    MONGO_CONFIG = {
        # "mongodb://0.0.0.0:27017"
        "username": "",
        "password": "",
        "host": "localhost",
        "port": 27017,
        "db": "2c",
    }
    DD_URL = "https://oapi.dingtalk.com/robot/send?access_token={0}"

    # 微信公众号订阅源，依赖项目：https://github.com/hellodword/wechat-feeds
    RSS_DICT = {
        "是不是很酷": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzU4NTIxODYwMQ==.xml",
        "caoz的梦呓": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzI0MjA1Mjg2Ng==.xml",
        "美团技术团队": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MjM5NjQ5MTI5OA==.xml",
        "阿里技术": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzIzOTU0NTQ0MA==.xml",
        "ThoughtWorks洞见": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MjM5MjY3OTgwMA==.xml",
        "小米技术": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzUxMDQxMDMyNg==.xml",
        "老胡的储物柜": "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/MzU4MTA0NDQ0Ng==.xml",
    }
