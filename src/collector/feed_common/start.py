"""
    Created by leeorz.
    Description：抓取目标rss，并解析rss条目，持久化到mongodb
    Changelog: all notable changes to this file will be documented
"""
import time

import feedparser

from src.collector.utils import load_data_to_articlles
from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import extract_core_html
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption, text_compress


def run(collect_config: dict):
    """rss解析，rss条目持久化

    Args:
        collect_config (dict, optional): 采集器配置
    """
    feeds_dict: dict = collect_config.get("feeds_dict")
    feeds_name: list = list(feeds_dict)
    delta_time = collect_config.get("delta_time", 1)
    for name in feeds_name:
        LOGGER.info(f"rss源 {name}: {feeds_dict[name]}")
        fd = feedparser.parse(feeds_dict[name])
        for entry in fd.entries:
            LOGGER.info(entry.link)
            # 休眠
            time.sleep(delta_time)
            resp_text = get_html_by_requests(
                url=entry.link,
                headers={"User-Agent": Config.LL_SPIDER_UA},
            )
            _, doc_core_html = extract_core_html(resp_text)
            doc_core_html_lib = text_compress(doc_core_html)
            input_data = {
                "doc_date": entry.get("published", ""),
                "doc_image": "",
                "doc_name": entry.get("title", ""),
                "doc_ts": int(time.time()),
                "doc_link": entry.get("link", ""),
                "doc_source_meta_list": [],
                "doc_keywords": " ",
                "doc_des": entry.get("description", ""),
                "doc_core_html": doc_core_html_lib,
                "doc_type": "article",
                "doc_author": "",
                "doc_source_name": name,
                "doc_id": md5_encryption(f"{entry.get('title', '')}_{name}"),
                "doc_source": "liuli_feed",
                "doc_source_account_nick": "",
                "doc_source_account_intro": "",
                "doc_content": "",
                "doc_html": "",
            }
            load_data_to_articlles(input_data)
    msg = "🤗 liuli_feed 采集器执行完毕"
    LOGGER.info(msg)
