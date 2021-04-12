#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：日志模块
    Changelog: all notable changes to this file will be documented
"""

import logging


def get_logger(name="2c"):
    """
    获取日志
    :param name:
    :return:
    """
    logging_format = f"[%(asctime)s] %(levelname)-5s %(name)-{len(name)}s "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    )
    return logging.getLogger(name)


LOGGER = get_logger()
