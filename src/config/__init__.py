"""
    Created by howie.hu at 2023-05-09.
    Description: 配置文件
    Changelog: all notable changes to this file will be documented
"""

import json
import os

from src.utils.log import get_logger

from .config import Config


def init_env_config() -> dict:
    """
    加载 liuli 环境，主要针对数据库和初始用户名（密码启动成功后自行设置）
    """
    ll_env_config = {}
    with open(
        os.path.join(Config.CACHE_DIR, "ll_env.json"), "r", encoding="utf8"
    ) as fp:
        ll_env_config: dict = json.load(fp)
    ll_env_config.update({"username": "liuli"})
    return ll_env_config


API_LOGGER = get_logger("Liuli API")
LOGGER = get_logger("Liuli")
