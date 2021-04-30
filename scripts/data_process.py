#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：从广告文本提取抽取标题作为训练样本
    Changelog: all notable changes to this file will be documented
"""
import os
import time

import pandas as pd

from src.collector import fetch_keyword_list
from src.config import Config


def gen_keyword_ads(
    s_path: str = "../.files/datasets/ads.csv",
    c_path: str = "../.files/datasets/clean_ads.csv",
):
    """
    广告文本提取关键词，前提是相关文本遵循了2c定义的数据集格式
    :param s_path: 源路径
    :param c_path: 目标关键词提取后的路径
    :return:
    """

    s_df = pd.read_csv(s_path)
    c_df = pd.read_csv(c_path)
    s_data_res, c_data_res = [], []

    for each in c_df.values.tolist():
        c_data_res.append(
            {"title": each[0], "keywords": each[1],}
        )

    for each in s_df.values.tolist():
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
                    c_data_res.append(
                        {"title": title, "keywords": " ".join(keyword_list)}
                    )
        s_data_res.append(cur_data)

    # 持久化
    pd.DataFrame(s_data_res).to_csv(s_path, index=False)
    pd.DataFrame(c_data_res).to_csv(c_path, index=False)


def clean_sample():
    """
    对样本进行清洗
    """
    clean_ads_path = "../.files/datasets/clean_ads.csv"
    clean_df = pd.read_csv(clean_ads_path)
    print(clean_df.head())


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
    # url = "https://jishuin.proginn.com/p/763bfbd54d15"
    # keyword_list = fetch_keyword_list(url)
    # print(keyword_list)
    gen_keyword_ads()
    # clean_sample()
