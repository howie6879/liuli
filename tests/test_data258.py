"""
    Created by howie.hu at 2022-06-05.
    Description: data258 测试脚本
    Changelog: all notable changes to this file will be documented
"""


import time

import requests

from src.collector.wechat.data258_ruia_start import exec_js_data258

url = "https://mp.data258.com/wx?id=d3da5e051e7ae38315c8b99556726ced&t=5lk2PVxxwiA6EiUu8BKRdIewSaV8EJYhM8Byk5aGuhEkvJCU5cQkCkmWf12foajABRhpSlDRTS6qmv63gw%3D%3D"


headers = {
    "Host": "mp.data258.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Referer": "https://mp.data258.com/article/category/howie_locker",
}


def get_proxy(flag: bool = False):
    """
    get random proxy from proxypool
    :return: proxy
    """
    if flag:
        proxy = ""
        proxies = {
            "http": f"{proxy}",
            "https": f"{proxy}",
        }
    else:
        proxies = None

    return proxies


def test_times():
    """反爬措施测试"""
    res = None
    try:
        proxies = get_proxy()
        print("get random proxy", proxies)
        resp = requests.get(url=url, headers=headers, proxies=proxies)
        html = resp.text
        if len(str(html)) > 100:
            res = exec_js_data258(html=html)

    except Exception as e:
        print(f"抓取失败! {e}")

    return res


if __name__ == "__main__":
    # while True:
    #     res = test_times()
    #     time.sleep(2)
    #     print(res)
    nums = 0
    while True:
        res = test_times()
        time.sleep(2)
        print(res)
        if res:
            nums += 1
        else:
            break
    print(f"单IP上限次数：{nums}")
