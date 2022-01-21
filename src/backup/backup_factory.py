"""
    Created by howie.hu at 2022-01-16.
    Description: 备份器工厂
    支持备份方式如下：
        - Github
    命令：PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/backup/backup_factory.py
    Changelog: all notable changes to this file will be documented
"""


from importlib import import_module

from src.backup.base import BackupBase
from src.utils import LOGGER
from src.utils.tools import string_camelcase


def backup_factory(backup_type: str, backup_config: dict) -> BackupBase:
    """
    备份器工厂函数
    :param backup_type: 备份类型
    :param backup_config: 备份配置
    :return:
    """
    backup_ins = None
    try:
        backup_class_name = f"{backup_type}_backup"
        backup_module = import_module(f"src.backup.{backup_class_name}")
        # 备份类实例化
        backup_ins = getattr(backup_module, string_camelcase(backup_class_name))(
            backup_config=backup_config
        )
    except ModuleNotFoundError:
        LOGGER.error(f"目标备份类型不存在 {backup_type} - {backup_config}")
    return backup_ins


if __name__ == "__main__":
    test_backup_data = {
        "doc_id": "test",
        "doc_source": "liuli_wechat",
        "doc_source_name": "老胡的储物柜",
        "doc_name": "打造一个干净且个性化的公众号阅读环境",
        "doc_link": "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw",
    }

    backup = backup_factory(backup_type="mongodb", backup_config={})
    # backup = backup_factory(backup_type="github", backup_config={})

    backup.delete(
        doc_source="liuli_wechat",
        doc_source_name="老胡的储物柜",
        doc_name="打造一个干净且个性化的公众号阅读环境",
    )

    backup.backup(test_backup_data)
