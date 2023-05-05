"""
    Created by howie.hu at 2021-12-30.
    Description: 外部调用相关请求
    Changelog: all notable changes to this file will be documented
"""
import json

import cchardet
import requests

from src.utils import LOGGER


def get_html_by_phantomjs(url: str, sk_key: str):
    """
    基于 phantomjs 获取html
    """
    data = {
        "url": url,
        "renderType": "html",
        # "waitForSelector": "",
    }
    url = f"http://PhantomJScloud.com/api/browser/v2/{sk_key}/"
    html = ""
    try:
        req = requests.post(url, data=json.dumps(data), timeout=60)
        html = req.text
    except Exception as e:
        LOGGER.error(f"通过 Phantomjs 请求 {url} 失败! {e}")
    return html


def get_html_by_requests(url: str, params: dict = None, timeout: int = 3, **kwargs):
    """发起GET请求，获取文本

    Args:
        url (str): 目标网页
        params (dict, optional): 请求参数. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 3.
    """
    resp = send_get_request(url=url, params=params, timeout=timeout, **kwargs)
    text = None
    try:
        content = resp.content
        charset = cchardet.detect(content)
        text = content.decode(charset["encoding"])
    except Exception as e:
        LOGGER.exception(f"请求内容提取出错 - {url} - {str(e)}")
    return text


def send_get_request(url: str, params: dict = None, timeout: int = 3, **kwargs):
    """发起GET请求

    Args:
        url (str): 目标地址
        params (dict, optional): 请求参数. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 3.

    Returns:
        [type]: [description]
    """
    try:
        resp = requests.get(url, params, timeout=timeout, **kwargs)
    except Exception as e:
        resp = None
        LOGGER.exception(f"请求出错 - {url} - {str(e)}")
    return resp


def send_post_request(url: str, data: dict = None, timeout: int = 5, **kwargs) -> dict:
    """发起post请求

    Args:
        url (str): 目标地址
        data (dict, optional): 请求参数. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 5.

    Returns:
        dict: [description]
    """
    try:
        resp_dict = requests.post(
            url, data=json.dumps(data), timeout=timeout, **kwargs
        ).json()
    except Exception as e:
        resp_dict = {}
        LOGGER.error(f"请求出错：{e}")
    return resp_dict
