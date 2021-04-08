#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：模型父类
    Changelog: all notable changes to this file will be documented
"""


class ModelResponse:
    """
    模型响应父类，定义一些常用属性
    """

    def __init__(self):
        """
        属性初始化
        """
        self.model_name = ""
        # 0 正常 1 异常
        self.result = 0
        self.probability = 0.0
        # 特征字典
        # 基础key有：
        # - is_black:   是否黑名单
        # - is_white:   是否白名单
        # - text:       输入文本
        self.feature_dict = {}
