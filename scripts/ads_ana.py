#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：从广告文本提取抽取标题作为训练样本
    Changelog: all notable changes to this file will be documented
"""
import os
import time

from collections import Counter

import pandas as pd

from newspaper import Article

from src.config import Config


def get_keyword(url: str):
    """
    获取文章简要说明作为样本
    失败就会出现 ['该内容已被发布者删除']
    :param url:
    :return:
    """
    article = Article(url, language="zh")
    article.download()
    article.parse()

    article.nlp()
    print(article.keywords)


def csv2txt(target_path: str = ""):
    """
    提取广告CSV中的标题作为广告样本
    :param target_path:
    :return:
    """
    target_path = target_path or os.path.join(
        Config.MODEL_DIR, f"cos/train.{int(time.time())}.txt"
    )
    ads_path = "../.files/datasets/ads.csv"
    df = pd.read_csv(ads_path)

    # 查看重复样本
    # print(Counter(df["title"].values.tolist()))

    all_title = df["title"].drop_duplicates().values.tolist()
    with open(target_path, "w") as fp:
        for title in all_title:
            fp.write(title + "\n")
    print(f"{target_path} 写入成功，共 {len(all_title)} 条记录")


if __name__ == "__main__":
    # csv2txt()
    get_keyword("https://mp.weixin.qq.com/s/GacxVno-apw-5O6JfZ03nw")
