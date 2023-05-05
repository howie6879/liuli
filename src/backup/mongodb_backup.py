"""
    Created by howie.hu at 2022-01-19.
    Description: 基于MongoDB做备份
        - 命令：PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/backup/mongodb_backup.py
    Changelog: all notable changes to this file will be documented
"""
import time

from src.backup.base import BackupBase
from src.databases.mongodb_tools import mongodb_delete_many_data, mongodb_update_data
from src.utils import LOGGER
from src.utils.tools import text_compress


class MongodbBackup(BackupBase):
    """基于MongoDB进行文章备份"""

    def __init__(self, init_config: dict):
        """
        初始化相关变量
        :param init_config: {}
        """
        super().__init__(backup_type="mongodb", init_config=init_config or {})
        self.liuli_backup_coll = self.mongo_base.get_collection(
            coll_name="liuli_backup"
        )
        # 是否每次更新都强制备份，默认只备份一次
        self.force_backup = init_config.get("force_backup", False)

    def save(self, backup_data: dict) -> bool:
        """执行备份动作

        Args:
            backup_data (dict): 备份数据

        Returns:
            bool: 是否成功
        """
        # 以下字段必须存在
        doc_source = backup_data["doc_source"]
        doc_source_name = backup_data["doc_source_name"]
        doc_name = backup_data["doc_name"]
        # 源文件
        doc_html = backup_data["doc_html"]

        file_msg = f"{doc_source}/{doc_source_name}/{doc_name}"
        file_path = f"{file_msg}.html"
        is_backup = self.is_backup(
            doc_source=doc_source,
            doc_source_name=doc_source_name,
            doc_name=doc_name,
        )

        # 未备份过或者强制备份下将继续执行
        if not is_backup or self.force_backup:
            filter_dict = {
                "doc_source": doc_source,
                "doc_source_name": doc_source_name,
                "doc_name": doc_name,
            }
            update_data = {
                "$set": {
                    **filter_dict,
                    **{"ts": int(time.time()), "content": text_compress(doc_html)},
                }
            }
            db_update_res = mongodb_update_data(
                coll_conn=self.liuli_backup_coll,
                filter_dict=filter_dict,
                update_data=update_data,
                upsert=True,
            )
            if db_update_res["status"]:
                msg = f"Backup({self.backup_type}): {file_path} 备份成功！"
                # 保存当前文章状态
                self.save_backup(
                    doc_source=doc_source,
                    doc_source_name=doc_source_name,
                    doc_name=doc_name,
                )
            else:
                msg = f"Backup({self.backup_type}): {file_path} 备份失败！{db_update_res['info']}"

        else:
            msg = f"Backup({self.backup_type}): {file_path} 已存在！"
        LOGGER.info(msg)

    def delete(self, doc_source: str, doc_source_name: str, doc_name: str) -> bool:
        """删除某个文件

        Args:
            doc_source (str): 文章获取源
            doc_source_name (str): 文章源
            doc_name (str): 文章名字
        Returns:
            bool: 是否成功
        """
        file_path = f"{doc_source}/{doc_source_name}/{doc_name}.html"
        db_res = mongodb_delete_many_data(
            coll_conn=self.liuli_backup_coll,
            filter_dict={
                "doc_source": doc_source,
                "doc_source_name": doc_source_name,
                "doc_name": doc_name,
            },
        )
        op_res = True
        if db_res["status"]:
            LOGGER.info(f"Backup({self.backup_type}): {file_path} 删除成功！")
            # 删除当前文章状态
            self.delete_backup(
                doc_source=doc_source,
                doc_source_name=doc_source_name,
                doc_name=doc_name,
            )
        else:
            op_res = False
            LOGGER.error(
                f"Backup({self.backup_type}): {file_path} 删除失败！{db_res['info']}"
            )
        return op_res


if __name__ == "__main__":
    test_backup_data = {
        "doc_source": "liuli_wechat",
        "doc_source_name": "老胡的储物柜",
        "doc_name": "打造一个干净且个性化的公众号阅读环境",
        "doc_link": "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw",
        "doc_html": "Hello World2",
    }
    mongo_backup = MongodbBackup({"force_backup": True})
    mongo_backup.delete(
        doc_source="liuli_wechat",
        doc_source_name="老胡的储物柜",
        doc_name="打造一个干净且个性化的公众号阅读环境",
    )
    mongo_backup.save(test_backup_data)
