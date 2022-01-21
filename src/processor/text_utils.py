"""
    Created by howie.hu at 2021-12-30.
    Description: 通用处理函数
    Changelog: all notable changes to this file will be documented
"""

import os

import html2text

from readability import Document
from textrank4zh import TextRank4Keyword

from src.classifier import model_predict_factory
from src.common.remote import send_get_request
from src.config import Config
from src.databases import MongodbManager
from src.utils.log import LOGGER


def fetch_keyword_list(url_or_text: str = None):
    """
    获取文本的关键词列表
    :param url_or_text:
    :return:
    """
    if url_or_text.startswith("http"):
        resp = send_get_request(url_or_text)
        # TODO 当text为空时候需要进行处理
        text = html_to_text_h2t(resp.text) if resp else None
    else:
        text = url_or_text
    stop_file_path = os.path.join(
        os.path.join(Config.MODEL_DIR, "data"), "stop_words.txt"
    )
    tr4w = TextRank4Keyword(stop_words_file=stop_file_path)
    tr4w.analyze(text=text, lower=True, window=2)
    keyword_list = []
    for item in tr4w.get_keywords(20, word_min_len=2):
        keyword_list.append(item.word)

    return keyword_list


def html_to_text_h2t(html: str):
    """
    从html提取核心内容text
    :param html:
    :return:
    """
    doc = Document(html)
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = False
    h.unicode_snob = False
    text = h.handle(doc.summary())
    return text.strip()


def str_replace(text: str, before_str: str, after_str: str) -> str:
    """文本替换

    Args:
        text (str): 原始文本
        before_str (str): 替换前
        after_str (str): 替换后
    """
    return str(text).replace(before_str, after_str)


def update_ads_tag(is_force=False):
    """
    对订阅的文章进行广告标记
    :param is_force: 是否强制重新判决
    :return:
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="liuli_articles")
    if is_force:
        query = {}
    else:
        query = {"cos_model": {"$exists": False}}

    # 查找没有被标记的文章，基于相似度模型进行判断
    for each_data in coll.find(query):
        doc_name = each_data["doc_name"]
        doc_source_name = each_data["doc_source_name"]
        doc_content = each_data["doc_content"]
        doc_keywords = each_data.get("doc_keywords")

        if not doc_keywords:
            keyword_list = fetch_keyword_list(doc_content)
            doc_keywords = " ".join(keyword_list)
            each_data["doc_keywords"] = doc_keywords

        # 基于余弦相似度
        cos_model_resp = model_predict_factory(
            model_name="cos",
            model_path="",
            input_dict={"text": doc_name + doc_keywords, "cos_value": Config.COS_VALUE},
            # input_dict={"text": doc_name, "cos_value": Config.COS_VALUE},
        ).to_dict()
        each_data["cos_model"] = cos_model_resp
        if cos_model_resp["result"] == 1:
            LOGGER.info(
                f"[{doc_source_name}] {doc_name} 被识别为广告[{cos_model_resp['probability']}]，链接为：{each_data['doc_link']}"
            )
        coll.update_one(
            filter={"doc_id": each_data["doc_id"]},
            update={"$set": each_data},
            upsert=True,
        )


if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw"
    resp = send_get_request(url)
    text = html_to_text_h2t(resp.text)
    print(text)
    res = fetch_keyword_list(url)
    print(res)
