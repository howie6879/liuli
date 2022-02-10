"""
    Created by howie.hu at 2022-02-08.
    Description: 处理器测试用例
        - pytest -s tests/test_processor.py
    Changelog: all notable changes to this file will be documented
"""

from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import extract_chapters


def test_extract_chapters():
    """
    目录提取测试用例
    """
    chapter_url = "https://book.qidian.com/info/1010868264/#Catalog"
    # chapter_url = "https://www.iwurexs.com/read/309300/"
    resp_text = get_html_by_requests(
        chapter_url, headers={"User-Agent": Config.SPIDER_UA}
    )
    chapters_res = extract_chapters(chapter_url=chapter_url, html=resp_text)
    assert len(chapters_res) > 1
