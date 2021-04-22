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
from src.databases import MongodbManager


def fetch_keyword_list(url: str):
    """
    获取文章简要说明作为样本
    失败就会出现 ['该内容已被发布者删除']
    :param url:
    :return:
    """
    article = Article(url, language="zh")
    article.download()
    article.parse()
    tr4w = TextRank4Keyword()
    tr4w.analyze(
        text=article.text, lower=True, window=2, vertex_source="words_no_stop_words"
    )
    keyword_list = []
    for item in tr4w.get_keywords(20, word_min_len=2):
        keyword_list.append(item.word)

    return keyword_list


def gen_keyword_ads():
    """
    广告文本提取关键词
    :param url:
    :return:
    """

    ads_path = "../.files/datasets/ads.csv"
    clean_ads_path = "../.files/datasets/clean_ads.csv"
    df = pd.read_csv(ads_path)
    clean_df = pd.read_csv(clean_ads_path)

    ads_res = []
    clean_ads_res = []

    for each in clean_df.values.tolist():
        clean_ads_res.append(
            {"title": each[0], "keywords": each[1],}
        )

    for each in df.values.tolist():
        title, url, is_process = each[0], each[1], each[2]
        cur_data = {
            "title": title,
            "url": url,
            "is_process": is_process,
        }
        if is_process == 0:
            # 进行提取，成功就改值为1
            keyword_list = fetch_keyword_list(url)
            if keyword_list:
                # 判断是否被删除
                if "发布者" in keyword_list and "删除" in keyword_list:
                    cur_data["is_process"] = "0"
                    print(f"{title} {url} 需要重新收集有效链接")
                else:
                    cur_data["is_process"] = "1"
                    clean_ads_res.append(
                        {"title": title, "keywords": ";".join(keyword_list)}
                    )
        ads_res.append(cur_data)

    # 持久化
    pd.DataFrame(ads_res).to_csv(ads_path, index=False)
    pd.DataFrame(clean_ads_res).to_csv(clean_ads_path, index=False)


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
    # url = "https://www.ershicimi.com/p/f4b00ac47a2b2fa2ce50719ed2787963"
    # keyword_list = fetch_keyword_list(url)
    # print(keyword_list)
    gen_keyword_ads()
