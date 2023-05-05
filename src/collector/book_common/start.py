"""
    Created by howie.hu at 2022-02-08.
    Description: 抓取目标链接的目录信息
        - 命令: PIPENV_DOTENV_LOCATION=./dev.env pipenv run python src/collector/book_common/start.py
    Changelog: all notable changes to this file will be documented
"""

import time

from src.collector.utils import load_data_to_articlles
from src.common.remote import get_html_by_phantomjs
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
    """书籍目录抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    book_dict: dict = collect_config["book_dict"]
    delta_time = collect_config.get("delta_time", 5)
    doc_source = collect_config.get("doc_source", 5)
    latest_chapter_nums = collect_config.get("latest_chapter_nums", 1)
    sk_key = Config.LL_SPIDER_PHANTOMJS_KEY
    for book_name, book_url in book_dict.items():
        resp_text = get_html_by_phantomjs(book_url, sk_key)
        all_chapters = extract_chapters(chapter_url=book_url, html=resp_text)
        latest_chapter_nums = (
            latest_chapter_nums
            if len(all_chapters) > latest_chapter_nums
            else len(all_chapters)
        )
        latest_chapter_list = all_chapters[-latest_chapter_nums:]
        for latest_chapter in latest_chapter_list:
            doc_name = latest_chapter.get("chapter_name")
            doc_link = latest_chapter.get("chapter_url")
            # 休眠
            time.sleep(delta_time)
            resp_text = get_html_by_phantomjs(
                doc_link,
                sk_key,
            )
            _, doc_core_html = extract_core_html(resp_text)
            # 压缩为二进制进行存储
            doc_core_html_lib = text_compress(doc_core_html)
            input_data = {
                "doc_date": "",
                "doc_image": "",
                "doc_name": doc_name,
                "doc_ts": int(time.time()),
                "doc_link": doc_link,
                "doc_source_meta_list": [],
                "doc_keywords": " ".join(
                    extract_keyword_list(html_to_text_h2t(resp_text))
                ),
                "doc_des": "",
                "doc_core_html": doc_core_html_lib,
                "doc_type": "book",
                "doc_author": "",
                "doc_source_name": book_name,
                "doc_id": md5_encryption(f"{doc_name}_{book_name}"),
                "doc_source": doc_source,
                "doc_source_account_nick": "",
                "doc_source_account_intro": "",
                "doc_content": "",
                "doc_html": "",
            }
            # 持久化，必须执行
            load_data_to_articlles(input_data)
    msg = "🤗 liuli_book 采集器执行完毕"
    LOGGER.info(msg)


if __name__ == "__main__":
    t_cc = {
        "book_dict": {"谁还不是个修行者了": "https://www.asxs.com/view/162095/"},
        "delta_time": 5,
        "latest_chapter_nums": 3,
        "doc_source": "liuli_book",
    }
    run(t_cc)
