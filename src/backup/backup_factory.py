"""
    Created by howie.hu at 2022-01-16.
    Description: 备份器工厂
    支持备份方式如下：
        - Github
        - MongoDB
    命令：PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/backup/backup_factory.py
    Changelog: all notable changes to this file will be documented
"""


from importlib import import_module

from src.backup.base import BackupBase
from src.utils import LOGGER
from src.utils.tools import string_camelcase


def backup_factory(backup_type: str, init_config: dict) -> BackupBase:
    """
    备份器工厂函数
    :param backup_type: 备份类型
    :param init_config: 备份配置
    :return:
    """
    backup_ins = None
    try:
        backup_class_name = f"{backup_type}_backup"
        backup_module = import_module(f"src.backup.{backup_class_name}")
        # 备份类实例化
        backup_ins = getattr(backup_module, string_camelcase(backup_class_name))(
            init_config=init_config
        )
    except ModuleNotFoundError as e:
        LOGGER.error(f"目标备份类型不存在 {backup_type} - {init_config} - {e}")
    return backup_ins
