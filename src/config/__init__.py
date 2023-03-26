#!/usr/bin/env python
"""
 Created by howie.hu at 2021/4/7.
"""
import json
import os

from src.utils.log import get_logger

from .config import Config


def init_db_config() -> dict:
    """
    加载 liuli 环境
    """
    ll_db_config = {}
    with open(os.path.join(Config.CACHE_DIR, "ll_db.json"), "r", encoding="utf8") as fp:
        ll_db_config: dict = json.load(fp)

    return ll_db_config


API_LOGGER = get_logger("Liuli API")
