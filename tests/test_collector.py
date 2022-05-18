"""
    Created by howie.hu at 2021-12-20.
    Description: 采集器测试用例
        - pytest -s tests/test_collector.py
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import os
import re

import execjs

from src.collector.wechat.items import SGWechatItem, WechatItem
from src.config import Config

ROOT_DIR = os.path.dirname(Config.BASE_DIR)
TEST_DIR = os.path.join(ROOT_DIR, "tests")
HTML_DIR = os.path.join(TEST_DIR, "html_demo")


async def call_sg_item(html: str) -> list:
    """调用搜狗Item类

    Args:
        html (str): HTML内容

    Returns:
        list: 返回结果列表
    """
    item_list = []
    async for item in SGWechatItem.get_items(html=html):
        item_list.append(item)
    return item_list


def read_html(html_name: str) -> str:
    """读取HTML目录下的相关文件

    Args:
        html_name (str): 文件名称

    Returns:
        str: HTML内容
    """
    html_path = os.path.join(HTML_DIR, html_name)
    HTML = ""
    with open(html_path, mode="r", encoding="utf-8") as file:
        HTML = file.read()
    return HTML


def test_wechat_item():
    """测试微信Item"""
    html = read_html(html_name="wechat_demo.html")
    item: WechatItem = asyncio.run(WechatItem.get_item(html=html))
    print(item)
    assert item.doc_source_name == "老胡的储物柜"
    assert item.doc_source_account_nick == "howie_locker"
    assert item.doc_source_account_intro == "编程、兴趣、生活"


def test_sg_wechat_single_item():
    """测试 SGWechatItem 单行"""
    html = read_html(html_name="single.html")
    res = asyncio.run(call_sg_item(html))
    assert res[0].wechat_name == "老胡的储物柜"
    assert res[0].latest_title == "我的周刊(第018期)"


def test_sg_wechat_multiple_item():
    """测试 SGWechatItem 多行"""
    html = read_html(html_name="multiple.html")
    res = asyncio.run(call_sg_item(html))
    assert res[0].wechat_name == "Python编程"
    assert res[0].latest_title == "漫画|结对编程实在太可怕了!!"


def test_data258_js2wechat():
    """测试data258js解密"""

    html = """
    <script>
		layui.use(['layer', 'form','fly','flow'], function(){
        var form = layui.form;
        var $ = layui.jquery;
        var layer = layui.layer;
        var fly = layui.fly;
        var flow = layui.flow;
        var index = layer.load();
    });
    function _0x2952(_0x581a6f,_0x2c2561){var _0x2c7f84=_0x2c7f();return _0x2952=function(_0x295281,_0x53c8c2){_0x295281=_0x295281-0x9f;var _0x3cf917=_0x2c7f84[_0x295281];return _0x3cf917;},_0x2952(_0x581a6f,_0x2c2561);}var _0x494214=_0x2952;(function(_0x2260c2,_0x3b9c32){var _0x26e81a=_0x2952,_0x14b659=_0x2260c2();while(!![]){try{var _0xeda0ee=parseInt(_0x26e81a(0xbd))/0x1*(parseInt(_0x26e81a(0xa9))/0x2)+parseInt(_0x26e81a(0xbc))/0x3*(-parseInt(_0x26e81a(0xad))/0x4)+parseInt(_0x26e81a(0xae))/0x5*(parseInt(_0x26e81a(0xbf))/0x6)+-parseInt(_0x26e81a(0xac))/0x7*(parseInt(_0x26e81a(0xb8))/0x8)+-parseInt(_0x26e81a(0xb2))/0x9+parseInt(_0x26e81a(0xa2))/0xa+-parseInt(_0x26e81a(0xb5))/0xb*(-parseInt(_0x26e81a(0xa0))/0xc);if(_0xeda0ee===_0x3b9c32)break;else _0x14b659['push'](_0x14b659['shift']());}catch(_0x44845e){_0x14b659['push'](_0x14b659['shift']());}}}(_0x2c7f,0x96cfa));function _0x2c7f(){var _0x10f30d=['9eed2ae10b','spider','11QGlNOI','com/s?__bi','com/','5049904LlKZVM','id=2247486','sessionid=','cb8e9f7633','2456436fUAvLL','87353ldpOuu','a178d505e2','200142fmkIQz','0#rd','cedb0b94&s','25257012LWLetK','http://mp.','855060VHDjNi','https://ww','002&idx=1&','href','8b2a5187f8','115eb&chks','44de173ee0','2mBPfoR','m=fd4cdb83','sn=b1cbe64','7HpgdNv','4gdfqfw','145qusmpr','NDQ0Ng==&m','weixin.qq.','cene=126&&','10594719pVVGPN'];_0x2c7f=function(){return _0x10f30d;};return _0x2c7f();}window[_0x494214(0xb4)]?location[_0x494214(0xa5)]=_0x494214(0xa3)+'w.data258.'+_0x494214(0xb7):setTimeout(function(){var _0x161b21=_0x494214;location[_0x161b21(0xa5)]=_0x161b21(0xa1)+_0x161b21(0xb0)+_0x161b21(0xb6)+'z=MzU4MTA0'+_0x161b21(0xaf)+_0x161b21(0xb9)+_0x161b21(0xa4)+_0x161b21(0xab)+_0x161b21(0xbb)+_0x161b21(0xa6)+_0x161b21(0xa7)+_0x161b21(0xaa)+'ca3b529578'+'eacdf6a4a1'+_0x161b21(0xb3)+_0x161b21(0xa8)+_0x161b21(0xbe)+'9db4dd2d03'+_0x161b21(0x9f)+_0x161b21(0xb1)+_0x161b21(0xba)+_0x161b21(0xc0);},0x5dc);

	</script>
    """
    js_text = """
    window = {};
    location = {
    href: null,
    };
    """
    js_text += re.compile(r"\}\);(.*?)</script>", re.S).search(html)[1]
    js_text += re.compile(r":setTimeout\(function\(\){(.*?);},").search(html)[1]
    js = execjs.compile(js_text)
    res = js.eval("location")
    print(res["href"])
    assert (
        res["href"]
        == "http://mp.weixin.qq.com/s?__biz=MzU4MTA0NDQ0Ng==&mid=2247486002&idx=1&sn=b1cbe64cb8e9f76338b2a5187f8115eb&chksm=fd4cdb83ca3b529578eacdf6a4a19eed2ae10b44de173ee0a178d505e29db4dd2d03cedb0b94&scene=126&&sessionid=0#rd"
    )
