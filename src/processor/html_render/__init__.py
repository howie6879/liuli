"""
    Created by howie.hu at 2022-02-09.
    Description: 将常用文章渲染成html
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/processor/html_render/__init__.py
    Changelog: all notable changes to this file will be documented
"""
import os

from string import Template

from src.config import Config


def render_book_html(
    doc_source_name: str, doc_name: str, doc_content: str, theme: str = "book_owllook"
) -> str:
    """将抓取的元数据渲染成html

    Args:
        doc_source_name (str): 书籍名称
        doc_name (str): 书籍当前章节
        doc_content (str): 书籍当前内容
        theme (str): 渲染主题
    Returns:
        str: html
    """
    book_tmpl_path = os.path.join(Config.PROC_HTML_TMPL_DIR, f"{theme}.tmpl")
    with open(book_tmpl_path, "rb") as fp:
        raw = fp.read().decode("utf8")
    render_dict = {
        "html_title": f"{doc_source_name}-{doc_name}",
        "article_title": doc_name,
        "article_content": doc_content,
    }
    raw_html = Template(raw).substitute(render_dict)
    return raw_html


if __name__ == "__main__":
    s_data = {
        "doc_id": "13611259dd2caf25ebdec506c11032ba",
        "doc_author": "",
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
    r_raw_html = render_book_html("诡秘之主", "第四十一章 新的旅程", "")
    print(r_raw_html)
