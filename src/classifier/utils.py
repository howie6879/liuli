#!/usr/bin/env python
"""
    Created by howie.hu at 2021/04/27.
    Description: 模型相关通用工具函数
    Changelog: all notable changes to this file will be documented
"""
import os

import pandas as pd

from pypinyin import lazy_pinyin

from src.config import Config
from src.utils import load_text_to_list


def text2py(text):
    """
    中文文本转成拼音
    :param text:
    :return:
    """

    return "".join(lazy_pinyin(text))


def ads2txt(target_path: str = ""):
    """
    提取广告CSV中的标题作为广告样本
    :param target_path: 目标写入地址
    :return:
    """
    target_path = target_path or os.path.join(Config.MODEL_DIR, f"cos/train.txt")
    his_text_list = load_text_to_list(target_path)

    ads_path = os.path.join(Config.DS_DIR, "clean_ads.csv")
    df = pd.read_csv(ads_path)

    df["text"] = df["title"] + " " + df["keywords"]

    # all_text = set(df["title"].drop_duplicates().values.tolist() + his_text_list)
    all_text = set(df["text"].drop_duplicates().values.tolist() + his_text_list)

    with open(target_path, "w") as fp:
        for title in all_text:
            fp.write(title + "\n")

    print(f"{target_path} 写入成功，共 {len(all_text)} 条记录")


def gen_alphabet() -> str:
    """
    基于 .files/datasets 目录下的数据集，生成字幕文件
    i（,l）h《$9a～“g」”』~.?j7·x)—;}'》k`|&>rvf5*0q：de{/":？w3，_ys#｜^8-『】[41%!<「bn+(om…6【tp=！c@uz]\2
    """
    # 基础字符列表
    character_list = list(
        "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
    )

    for file_name in ["final_ads.csv", "final_normal.csv"]:
        full_path = os.path.join(Config.DS_DIR, file_name)
        df = pd.read_csv(full_path)
        for each in df["text"].values:
            for word in each.strip().split(" "):
                for character in list(word):
                    if character:
                        character_list.append(character.lower())

    return "".join(list(set(character_list)))


if __name__ == "__main__":
    # from collections import Counter
    #
    # df = pd.read_csv(os.path.join(Config.DS_DIR, "clean_ads.csv"))
    # print(Counter(df["title"].values.tolist()))

    ads2txt()
    # character_str = gen_alphabet()
    # print(character_str)
