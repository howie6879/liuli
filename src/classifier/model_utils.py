#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-27.
    Description: 模型相关通用工具函数
    Changelog: all notable changes to this file will be documented
"""
from pypinyin import lazy_pinyin

def text2py(text):
    """
    中文文本转成拼音
    :param text:
    :return:
    """

    return "".join(lazy_pinyin(text))


def gen_alphabet() -> list:
    """
    基于 .files/datasets 目录下的数据集，生成字幕文件
    """
    character_list = []

    for each in df["text"].values:
        for word in each[0].strip().split(" "):
            for character in list(word):
                if character:
                    character_list.append(character.lower())
    return character_list