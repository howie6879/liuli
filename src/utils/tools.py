#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/7.
    Description：通用函数
    Changelog: all notable changes to this file will be documented
"""

import hashlib


def md5_encryption(string: str) -> str:
    """
    对字符串进行md5加密
    :param string: 加密目标字符串
    :return:
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()
