#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：样本处理脚本
    Changelog: all notable changes to this file will be documented
"""

import os

import pandas as pd

from src.classifier import ads2txt, text2py
from src.collector import extract_keyword_list
from src.config import Config
from src.databases import MongodbManager
from src.utils import load_text_to_list


def gen_final_sample():
    """
    将样本做最后的拼音处理
    :return:
    """
    for sample in [("clean_ads.csv", 1), ("clean_normal.csv", 2)]:
        file_name, label = sample
        print(f"正在处理文件 {file_name}")
        full_path = os.path.join(Config.DS_DIR, file_name)
        df = pd.read_csv(full_path)
        df["text"] = df["title"] + df["keywords"]
        df["text"] = df["text"].apply(text2py)
        df["label"] = str(label)
        # 删除无关列
        df.drop(["title", "keywords"], axis=1, inplace=True)
        df.to_csv(full_path.replace("clean", f"final"), index=False)


def gen_keyword_sample(
    s_path: str = f"{Config.DS_DIR}/ads.csv",
    c_path: str = f"{Config.DS_DIR}/clean_ads.csv",
):
    """
    广告文本提取关键词，前提是相关文本遵循了liuli定义的数据集格式
    :param s_path: 源路径
    :param c_path: 目标关键词提取后的路径
    :return:
    """
    # 根据标题去重
    s_df = pd.read_csv(s_path).drop_duplicates(subset=["title"])
    c_df = pd.read_csv(c_path).drop_duplicates(subset=["title"])
    s_data_res, c_data_res = [], []

    for each in c_df.values.tolist():
        c_data_res.append(
            {
                "title": each[0],
                "keywords": each[1],
            }
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
            keyword_list = extract_keyword_list(url)
            print(keyword_list)
            if keyword_list:
                # 判断是否被删除
                if keyword_list and "发布者" in keyword_list and "删除" in keyword_list:
                    cur_data["is_process"] = "0"
                    print(f"{title} {url} 需要重新收集有效链接")
                else:
                    cur_data["is_process"] = "1"
                    keywords = " ".join(keyword_list)
                    c_data_res.append({"title": title, "keywords": keywords})
                    print(f"新增成功：{title} {url} {keywords}")
        s_data_res.append(cur_data)

    # 持久化
    pd.DataFrame(s_data_res).to_csv(s_path, index=False)
    pd.DataFrame(c_data_res).to_csv(c_path, index=False)


def gen_normal_sample(nums: int = None):
    """
    生成正常样本数据
    :param nums: 样本数量，默认数量取异常样本
    :return:
    """
    if nums is None:
        ads_path = os.path.join(Config.DS_DIR, "clean_ads.csv")
        ads_title_list = load_text_to_list(ads_path)
        nums = len(ads_title_list) - 1
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.LL_MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="liuli_articles")
    query = {"cos_model.result": 0, "doc_source_name": "真没什么逻辑"}
    normal_path = os.path.join(Config.DS_DIR, "normal.csv")
    for each_data in coll.aggregate([{"$match": query}, {"$sample": {"size": nums}}]):
        title = each_data["doc_name"]
        url = each_data["doc_link"]
        title = f'"{title}"' if "," in title else title
        info = f"{title},{url},0\n"
        print(info)
    # with open(normal_path, "w") as fp:
    #     fp.write("title,url,is_process\n")
    #     for each_data in coll.aggregate(
    #         [{"$match": query}, {"$sample": {"size": nums}}]
    #     ):
    #         title = each_data["doc_name"]
    #         url = each_data["doc_link"]
    #         title = f'"{title}"' if "," in title else title
    #         info = f"{title},{url},0\n"
    #         fp.write(info)


if __name__ == "__main__":
    # url = "https://jishuin.proginn.com/p/763bfbd54d15"
    # keyword_list = extract_keyword_list(url)
    # print(keyword_list)
    gen_keyword_sample()
    # ads2txt()
    # gen_keyword_sample(
    #     s_path=f"{Config.DS_DIR}/normal.csv",
    #     c_path=f"{Config.DS_DIR}/clean_normal.csv",
    # )
    # gen_normal_sample()
    # gen_final_sample()
