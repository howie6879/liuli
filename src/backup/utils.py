"""
    Created by howie.hu at 2022-01-25.
    Description: 存储器通用函数
    Changelog: all notable changes to this file will be documented
"""


from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.html_render import render_book_html
from src.utils.tools import text_decompress


def get_bak_doc_html(doc_data: dict, doc_html_type: str = "default") -> str:
    """返回不同doc_html类型下的最终html

    Args:
        doc_html_type (str): 各种获取doc_html的方式
            - default: 默认，获取doc_data里面的doc_html数据，不存在就使用online
            - online: 进行网络获取
            - book: 进行二次渲染，这里是渲染成书籍阅读主题
        doc_data (dict): 文章数据

    Returns:
        str: 处理后的 doc_html
    """
    # 获取原始文本内容
    doc_link = doc_data["doc_link"]
    online_func = lambda url: get_html_by_requests(
        url=url, headers={"User-Agent": Config.SPIDER_UA}
    )
    if doc_html_type == "online":
        doc_html = online_func(doc_link)
    elif doc_html_type == "book":
        doc_source_name = doc_data.get("doc_source_name", "")
        doc_name = doc_data.get("doc_name", "")
        doc_core_html = text_decompress(doc_data.get("doc_core_html", ""))
        doc_html = render_book_html(doc_source_name, doc_name, doc_core_html)
    else:
        # 本地模式
        doc_html = text_decompress(doc_data.get("doc_html")) or online_func(doc_link)

    return doc_html
