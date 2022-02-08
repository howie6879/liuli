"""
    Created by howie.hu at 2022-02-08.
    Description: 处理器测试用例
        - pytest -s tests/test_processor.py
    Changelog: all notable changes to this file will be documented
"""

from operator import le

from src.common.remote import send_get_request
from src.processor.text_utils import extract_chapters


def test_extract_chapters():
    """
    目录提取测试用例
    """
    chapter_url = "https://book.qidian.com/info/1010868264/#Catalog"
    # chapter_url = "https://www.yruan.com/article/38563.html"
    resp = send_get_request(chapter_url)
    chapters_res = extract_chapters(chapter_url=chapter_url, html=resp.text)
    assert len(chapters_res) > 1
