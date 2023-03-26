"""
    Created by howie.hu at 2021-12-30.
    Description: 通用处理函数
    Changelog: all notable changes to this file will be documented
"""
import os
import re

from urllib.parse import urljoin

import html2text
import jieba
import jieba.analyse

from bs4 import BeautifulSoup
from readability import Document

from src.classifier import model_predict_factory
from src.common.remote import get_html_by_requests, send_get_request
from src.config import Config
from src.databases import MongodbManager
from src.utils.log import LOGGER


def ad_marker(
    cos_value: float = 0.6,
    is_force=False,
    basic_filter=None,
    **kwargs,
):
    """对订阅的文章进行广告标记

    Args:
        cos_value (str): 0.6
        basic_filter (dict): {} 查询条件
        is_force (bool): 是否强制重新判决
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.LL_MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="liuli_articles")
    if is_force:
        query = {}
    else:
        query = {"cos_model": {"$exists": False}}

    query.update(basic_filter or {})

    # 查找没有被标记的文章，基于相似度模型进行判断
    for each_data in coll.find(query):
        doc_name = each_data["doc_name"]
        doc_source_name = each_data["doc_source_name"]
        doc_content = each_data["doc_content"]
        doc_keywords = each_data.get("doc_keywords")

        if not doc_keywords:
            keyword_list = extract_keyword_list(doc_content)
            doc_keywords = " ".join(keyword_list)
            each_data["doc_keywords"] = doc_keywords

        # 基于余弦相似度
        cos_model_resp = model_predict_factory(
            model_name="cos",
            model_path="",
            input_dict={"text": doc_name + doc_keywords, "cos_value": cos_value},
            # input_dict={"text": doc_name, "cos_value": Config.LL_COS_VALUE},
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


def extract_chapters(chapter_url, html):
    """
    通用解析小说目录
    :param chapter_url: 小说目录页url
    :param res: 当前页面html
    :return:
    """
    # 参考https://greasyfork.org/zh-CN/scripts/292-my-novel-reader
    chapters_reg = (
        r"(<a\s+.*?>.*第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集].*?</a>)"
    )
    # 这里不能保证获取的章节分得很清楚，但能保证这一串str是章节目录。可以利用bs安心提取a
    chapters_res = re.findall(chapters_reg, str(html), re.I)
    str_chapters_res = "\n".join(chapters_res)
    chapters_res_soup = BeautifulSoup(str_chapters_res, "html5lib")
    all_chapters = []
    for link in chapters_res_soup.find_all("a"):
        each_data = {}
        cur_chapter_url = urljoin(chapter_url, link.get("href")) or ""
        cur_chapter_name = link.text or ""
        if valid_chapter_name(cur_chapter_name):
            each_data["chapter_url"] = cur_chapter_url
            each_data["chapter_name"] = cur_chapter_name
            all_chapters.append(each_data)
    # 去重
    all_chapters_sorted = []
    for index, value in enumerate(all_chapters):
        if value not in all_chapters[index + 1 :]:
            all_chapters_sorted.append(value)
    return all_chapters_sorted


def extract_core_html(html: str):
    """从文章类型提取核心HTML

    Args:
        html (str): raw html
    """
    doc = Document(html)
    return doc.title(), doc.summary()


def extract_keyword_list(url_or_text: str = None):
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
    jieba.analyse.set_stop_words(stop_file_path)
    # keyword_list = jieba.analyse.extract_tags(text, topK=20)
    keyword_list = jieba.analyse.textrank(text, topK=20)

    # from textrank4zh import TextRank4Keyword
    # tr4w = TextRank4Keyword(stop_words_file=stop_file_path)
    # tr4w.analyze(text=text, lower=True, window=2)
    # keyword_list = []
    # for item in tr4w.get_keywords(20, word_min_len=2):
    #     keyword_list.append(item.word)

    return keyword_list


def html_to_text_h2t(html: str):
    """
    从html提取核心内容text
    :param html:
    :return:
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = False
    h.unicode_snob = False
    _, summary = extract_core_html(html)
    text = h.handle(summary)
    return text.strip()


def str_replace(text: str, before_str: str, after_str: str) -> str:
    """文本替换

    Args:
        text (str): 原始文本
        before_str (str): 替换前
        after_str (str): 替换后
    """
    return str(text).replace(before_str, after_str)


def valid_chapter_name(chapter_name):
    """
    判断目录名称是否合理
    Args:
        chapter_name ([type]): [description]
    """
    for each in ["目录"]:
        if each in chapter_name:
            return False
    return True


if __name__ == "__main__":
    # url = "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw"
    url = "https://www.yruan.com/article/38563/28963588.html"
    t_text = get_html_by_requests(url)
    # doc = Document(text)
    # print(doc.title(), doc.short_title(), dir(doc))
    # print(doc.summary())
    res_text = html_to_text_h2t(t_text)
    # print(res_text)
    res = extract_keyword_list(res_text)
    print(res)
