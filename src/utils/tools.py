"""
    Created by howie.hu at 2021/4/7.
    Description：通用函数
    Changelog: all notable changes to this file will be documented
"""
import hashlib
import random
import re
import socket
import string
import time
import zlib


def gen_random_str(length) -> str:
    """
    生成随机位数字符串
    Returns:
        str: 字符串
    """
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def get_ip():
    """
    获取本机IP
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def md5_encryption(string: str) -> str:
    """
    对字符串进行md5加密
    :param string: 加密目标字符串
    :return:
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


def is_contain_text(text: str, text_list: list) -> bool:
    """
    判断输入的本文是否被文本列表包含
    :param text: 文本
    :param text_list: 文本列表
    :return:
    """
    if text:
        for each in text_list:
            if each in text:
                return True
    return False


def load_text_to_list(file_path) -> list:
    """
    加载文本返回列表
    :param file_path:
    :return:
    """
    text_list = []
    with open(file_path, encoding="utf-8") as fp:
        for line in fp:
            line = line.replace("\n", "").strip()
            if line:
                text_list.append(line)
    return text_list


def string_camelcase(string: str) -> str:
    """
    方便普通字符串转化成大写开头命名的形式
    :param string:
    :return:
    """
    return re.compile(r"[^a-zA-Z\d]").sub("", string.title())


def text_compress(text: str) -> str:
    """对文本进行压缩

    Args:
        text (str): 待压缩文本

    Returns:
        str: 压缩后的文本
    """
    return zlib.compress(text.encode())


def text_decompress(text) -> str:
    """对文本进行解压

    Args:
        text (str or bytes): 待解压文本

    Returns:
        str: 解压后的文本
    """
    return zlib.decompress(text).decode() if type(text).__name__ == "bytes" else text


def read_file(file_path: str) -> list:
    """
    读取文本内容
    Args:
        file_path (str): 文件路径
    Returns:
        list: 每行文件内容组成的列表
    """
    try:
        with open(file_path, encoding="utf-8") as fp:
            file_list = [_.strip() for _ in fp.readlines()]
    except Exception as _:
        file_list = []
    return file_list


def ts_to_str_date(ts: int, ts_format: str = "%Y-%m-%d %H:%M:%S"):
    """
    时间戳转文本时间
    :param ts:
    :param ts_format:
    :return:
    """
    return time.strftime(ts_format, time.localtime(int(ts)))


if __name__ == "__main__":
    print(ts_to_str_date(1625024640.0))
    print(string_camelcase("github_backup"))
    print(get_ip())
    print(ts_to_str_date(time.time()))
    print(gen_random_str(32))
