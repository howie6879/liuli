"""
    Created by howie.hu at 2022-02-09.
    Description: 将常用文章渲染成html
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/processor/html_render/__init__.py
    Changelog: all notable changes to this file will be documented
"""
import os

from string import Template

from src.config import Config


def render_book_html(data: dict) -> str:
    """将抓取的元数据渲染成html

    Args:
        data (dict): 抓取的文章元数据
    Returns:
        str: html
    """
    book_tmpl_path = os.path.join(Config.PROC_HTML_TMPL_DIR, "book.tmpl")
    with open(book_tmpl_path, "rb") as fp:
        raw = fp.read().decode("utf8")
    doc_source_name = data.get("doc_source_name", "")
    doc_name = data.get("doc_name", "")
    doc_core_html = data.get("doc_core_html", "")
    render_dict = {
        "html_title": f"{doc_source_name}-{doc_name}",
        "article_title": doc_name,
        "article_content": doc_core_html,
    }
    raw_html = Template(raw).substitute(render_dict)
    return raw_html


if __name__ == "__main__":
    s_data = {
        "doc_id": "13611259dd2caf25ebdec506c11032ba",
        "doc_author": "",
        "doc_content": "",
        "doc_core_html": "w",
        "doc_date": "",
        "doc_des": "",
        "doc_image": "",
        "doc_keywords": "梅丽莎 小女孩 起来 阳光 模仿 出来 棺材 记起 醒来 姑姑 疑惑 看见 缝隙 仪式 盖子 神情 前些年 希望 选择 时代",
        "doc_link": "https://www.yruan.com/article/38563/28963588.html",
        "doc_name": "第四十一章 新的旅程",
        "doc_source": "liuli_book",
        "doc_source_account_intro": "",
        "doc_source_account_nick": "",
        "doc_source_meta_list": [],
        "doc_source_name": "诡秘之主",
        "doc_ts": 1644376985,
        "doc_type": "article",
    }
    raw_html = render_book_html(s_data)
    print(raw_html)
