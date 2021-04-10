#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：微信相关通用函数
    Changelog: all notable changes to this file will be documented
"""

from ruia import Request


async def get_wf_url():
    """
    获取 wechat-feeds 资源链接
    Github: https://github.com/hellodword/wechat-feeds
    :return:
    """
    url = "https://wechat.privacyhide.com/VERSION?"
    resp = await Request(url=url).fetch()
    version = str(await resp.text()).strip()
    return f"https://cdn.jsdelivr.net/gh/hellodword/wechat-feeds@{version}/details.json"
