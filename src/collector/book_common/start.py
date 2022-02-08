"""
    Created by howie.hu at 2022-02-08.
    Description: 抓取目标链接的目录信息
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/book_common/start.py
    Changelog: all notable changes to this file will be documented
"""

import time

from src.collector.utils import load_data_to_articlles
from src.common.remote import send_get_request
from src.processor.text_utils import extract_chapters
from src.utils.tools import md5_encryption


def run(collect_config: dict):
    """书籍目录抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    book_dict: dict = collect_config["book_dict"]
    for book_name, book_url in book_dict.items():
        resp = send_get_request(url=book_url)
        all_chapters = extract_chapters(chapter_url=book_url, html=resp.text)
        latest_chapter = all_chapters[-1] if all_chapters else {}
        doc_name = latest_chapter.get("chapter_name")
        doc_link = latest_chapter.get("chapter_url")
        data = {
            "doc_date": "",
            "doc_image": "",
            "doc_name": doc_name,
            "doc_ts": int(time.time()),
            "doc_link": doc_link,
            "doc_source_meta_list": [],
            "doc_keywords": "",
            "doc_des": "",
            "doc_core_html": "",
            "doc_type": "article",
            "doc_author": "",
            "doc_source_name": book_name,
            "doc_id": md5_encryption(f"{doc_name}_{book_name}"),
            "doc_source": "liuli_book",
            "doc_source_account_nick": "",
            "doc_source_account_intro": "",
            "doc_content": "",
        }
        load_data_to_articlles(input_data=data)


if __name__ == "__main__":
    t_cc = {
        "book_dict": {"诡秘之主": "https://www.yruan.com/article/38563.html"},
        "delta_time": 5,
    }
    run(t_cc)
