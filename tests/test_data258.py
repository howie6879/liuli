import re
import time

import execjs
import requests

url = "https://mp.data258.com/wx?id=d3da5e051e7ae38315c8b99556726ced&t=5lk2PVxxwiA6EiUu8BKRdIewSaV8EJYhM8Byk5aGuhEkvJCU5cQkCkmWf12foajABRhpSlDRTS6qmv63gw%3D%3D"


headers = {
    "Host": "mp.data258.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Referer": "https://mp.data258.com/article/category/howie_locker",
}


def get_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    proxy = ""
    proxies = {
        "http": f"{proxy}",
        "https": f"{proxy}",
    }
    return proxies


def test_times():
    """反爬措施测试"""
    try:
        proxies = get_proxy()
        print("get random proxy", proxies)
        resp = requests.get(url=url, headers=headers, proxies=proxies)
        html = resp.text
        if len(str(html)) > 100:
            # 构建加密js
            js_text = """
            window = {};
            location = {
            href: null,
            };
            """
            js_text += re.compile(r"\}\);(.*?)</script>", re.S).search(html)[1]
            js_text += re.compile(r":setTimeout\(function\(\){(.*?);},").search(html)[1]

            js = execjs.compile(js_text)
            res = js.eval("location")["href"]
        else:
            res = None

    except Exception as e:
        print(f"抓取失败! {e}")
        res = None
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
