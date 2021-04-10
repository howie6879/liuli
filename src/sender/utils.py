#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：分发器通用函数
    Changelog: all notable changes to this file will be documented
"""

import json

import requests

from src.utils import LOGGER


def send_post_request(url, data: dict = None, **kwargs) -> dict:
    """
    发起post请求
    :param url: 请求目标地址
    :param data: 请求参数
    :param kwargs:
    :return:
    """
    try:
        resp_dict = requests.post(url, data=json.dumps(data), **kwargs).json()
    except Exception as e:
        resp_dict = {}
        LOGGER.error(f"请求出错：{e}")
    return resp_dict
