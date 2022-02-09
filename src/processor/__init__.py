"""
    Created by howie.hu at 2022-01-13.
    Description: 常用中间件
    Changelog: all notable changes to this file will be documented
"""
from .rss_utils import to_rss
from .text_utils import (
    ad_marker,
    extract_core_html,
    extract_keyword_list,
    html_to_text_h2t,
    str_replace,
)

processor_dict = {
    "to_rss": to_rss,
    "ad_marker": ad_marker,
    "str_replace": str_replace,
}
