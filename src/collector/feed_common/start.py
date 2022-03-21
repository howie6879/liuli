import asyncio
import time

import feedparser

from src.collector.utils import load_data_to_articlles
from src.collector.wechat_sougou.items import WechatItem
from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import (
    extract_chapters,
    extract_core_html,
    extract_keyword_list,
    html_to_text_h2t,
)
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption, text_compress


def run(collect_config: dict):
    feeds_dict: dict = collect_config.get("feeds_dict")
    feeds_name: list = list(feeds_dict)
    delta_time = collect_config.get("delta_time", 5)
    for name in feeds_name:
        LOGGER.info(f"rss源 {name}: {feeds_dict[name]}")
        fd = feedparser.parse(feeds_dict[name])
        for entry in fd.entries:
            LOGGER.info(entry.link)
            resp_text = get_html_by_requests(
                url=entry.link, headers={"User-Agent": Config.SPIDER_UA}
            )
            _, doc_core_html = extract_core_html(resp_text)
            doc_core_html_lib = text_compress(doc_core_html)
            input_data = {
                "doc_date": entry.get('published', ''),
                "doc_image": "",
                "doc_name": entry.get('title', ''),
                "doc_ts": int(time.time()),
                "doc_link": entry.get('link',''),
                "doc_source_meta_list": [],
                "doc_keywords": " ",
                "doc_des": entry.get('description',""),
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
