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
import requests

from newspaper import Article
from textrank4zh import TextRank4Keyword, TextRank4Sentence

from src.config import Config


def fetch_keyword(url: str):
    """
    获取文章简要说明作为样本
    失败就会出现 ['该内容已被发布者删除']
    :param url:
    :return:
    """
    resp = requests.get(url)
    print(resp.text)
    # 进行关键词提取
    # article = Article(url, language="zh")
    # article.download()
    # article.parse()

    # print(article.html)
    #
    # tr4s = TextRank4Sentence()
    # tr4s.analyze(text=text, lower=True, source='all_filters')
    #
    # print()
    # print('摘要：')
    # for item in tr4s.get_key_sentences(num=3):
    #     print(item.index, item.weight, item.sentence)
    return ""


def gen_keyword_ads(url: str):
    """
    广告文本提取关键词
    :param url:
    :return:
    """

    ads_path = "../.files/datasets/ads.csv"
    df = pd.read_csv(ads_path)

    res = []

    for each in df.values.tolist():
        title, url, is_process = each[0], each[1], each[2]
        cur_data = {
            "title": title,
            "url": url,
            "is_process": is_process,
        }
        res.append(cur_data)
        if is_process == 0:
            # 进行提取，成功就改值为1
            keyword = fetch_keyword(url)
            # 判断是否被删除
            if "该内容已被发布者删除" in keyword:
                print(f"{title} {url} 需要重新收集有效链接")
            else:
                print(keyword)


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
    keyword = fetch_keyword("https://mp.weixin.qq.com/s/VhoRl9ispyAJCFnf9244Uw")
    print(keyword)
