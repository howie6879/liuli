#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：常用调度函数
    - 运行: 根目录执行，其中环境文件pro.env根据实际情况选择即可
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/schedule_task/all_tasks.py
    Changelog: all notable changes to this file will be documented
"""


from src.collector.collect_factory import collect_factory
from src.config import Config


def update_wechat_doc():
    """
    抓取最新的文章，然后持久化到数据库
    :param wechat_list:
    :return:
    """
    # TODO 统一的地方进行配置管理
    t_collect_type = "wechat_sougou"
    t_collect_config = {
        "wechat_list": Config.WECHAT_LIST,
        "delta_time": 5,
        # playwright
        "spider_type": "playwright",
    }
    collect_factory(t_collect_type, t_collect_config)


if __name__ == "__main__":
    # 第一次启动请执行
    update_wechat_doc()
    # 每次强制重新打标签
    # update_ads_tag(is_force=False)
    # send_doc()
