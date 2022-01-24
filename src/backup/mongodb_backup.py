"""
    Created by howie.hu at 2022-01-19.
    Description: 基于MongoDB做备份
        - 命令：PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/backup/mongodb_backup.py
    Changelog: all notable changes to this file will be documented
"""
import time

from src.backup.base import BackupBase
from src.common.remote import send_get_request
from src.databases.mongodb_tools import (
    mongodb_delete_many_data,
    mongodb_find,
    mongodb_update_data,
)
from src.utils import LOGGER


class MongodbBackup(BackupBase):
    """基于MongoDB进行文章备份"""

    def __init__(self, init_config: dict):
        """
        初始化相关变量
        :param send_config: {}
        """
        super().__init__(backup_type="mongodb", init_config=init_config or {})
        self.liuli_backup_coll = self.mongo_base.get_collection(
            coll_name="liuli_backup"
        )

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
        doc_text = backup_data["doc_text"]

        file_msg = f"{doc_source}/{doc_source_name}/{doc_name}"
        file_path = f"{file_msg}.html"
        is_backup = self.is_backup(
            doc_source=doc_source,
            doc_source_name=doc_source_name,
            doc_name=doc_name,
        )
        # 在数据库存在就默认线上必定存在，希望用户不操作这个仓库造成状态不同步
        if not is_backup:
            # 上传前做是否存在检测
            # 已存在的但是数据库没有状态需要重新同步
            filter_dict = {
                "doc_source": doc_source,
                "doc_source_name": doc_source_name,
                "doc_name": doc_name,
            }
            # 先判断文件是否存在
            db_find_res = mongodb_find(
                coll_conn=self.liuli_backup_coll,
                filter_dict=filter_dict,
                return_dict={"_id": 0},
            )
            if db_find_res["status"] and not db_find_res["info"]:
                # 没有备份过继续远程备份
                update_data = {
                    "$set": {
                        **filter_dict,
                        **{"ts": int(time.time()), "content": doc_text},
                    }
                }

                db_update_res = mongodb_update_data(
                    coll_conn=self.liuli_backup_coll,
                    filter_dict=filter_dict,
                    update_data=update_data,
                )
                if db_update_res["status"]:
                    msg = f"Backup({self.backup_type}): {file_path} 上传成功！"
                else:
                    msg = f"Backup({self.backup_type}): {file_path} 上传失败！{db_update_res['info']}"
            else:
                msg = f"Backup({self.backup_type}): {file_path} 已成功！"
            # 保存当前文章状态
            self.save_backup(
                doc_source=doc_source,
                doc_source_name=doc_source_name,
                doc_name=doc_name,
            )
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
        if db_res["status"]:
            LOGGER.info(f"Backup({self.backup_type}): {file_path} 删除成功！")
            # 删除当前文章状态
            self.delete_backup(
                doc_source=doc_source,
                doc_source_name=doc_source_name,
                doc_name=doc_name,
            )
        else:
            LOGGER.error(
                f"Backup({self.backup_type}): {file_path} 删除失败！{db_res['info']}"
            )


if __name__ == "__main__":
    test_backup_data = {
        "doc_source": "liuli_wechat",
        "doc_source_name": "老胡的储物柜",
        "doc_name": "打造一个干净且个性化的公众号阅读环境",
        "doc_link": "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw",
    }
    mongo_backup = MongodbBackup({})
    mongo_backup.save(test_backup_data)
    # mongo_backup.delete(
    #     doc_source="liuli_wechat",
    #     doc_source_name="老胡的储物柜",
    #     doc_name="打造一个干净且个性化的公众号阅读环境",
    # )
