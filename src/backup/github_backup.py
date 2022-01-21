"""
    Created by howie.hu at 2022-01-15.
    Description: 基于github做备份
        - 命令：s
    Changelog: all notable changes to this file will be documented
"""

from github import Github, GithubException

from src.backup.base import BackupBase
from src.common.remote import send_get_request
from src.config import Config
from src.utils import LOGGER


class GithubBackup(BackupBase):
    """基于Github进行文章备份"""

    def __init__(self, init_config: dict):
        """
        初始化相关变量
        :param send_config:
        """
        super().__init__(backup_type="github", init_config=init_config or {})
        github_token = init_config.get("github_token", Config.GITHUB_TOKEN)
        github_repo = init_config.get("github_repo", Config.GITHUB_REPO)
        g = Github(github_token)
        self.repo = g.get_repo(github_repo)

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
        # 有些html源文件比较大，直接网络请求然后保存
        doc_link = backup_data["doc_link"]

        file_msg = f"{doc_source}/{doc_source_name}/{doc_name}"
        file_path = f"{file_msg}.html"
        is_backup = self.is_backup(
            doc_source=doc_source,
            doc_source_name=doc_source_name,
            doc_name=doc_name,
        )

        # 在数据库存在就默认线上必定存在，希望用户不操作这个仓库造成状态不同步
        if not is_backup:
            # 没有备份过继续远程备份
            resp = send_get_request(url=doc_link)
            # 上传前做是否存在检测
            # 已存在的但是数据库没有状态需要重新同步
            try:
                # 先判断文件是否存在
                try:
                    _ = self.repo.get_contents(file_path)
                except Exception as e:
                    # 调试，先硬编码
                    before_str = 'data-src="'
                    after_str = 'src="https://images.weserv.nl/?url='
                    content = resp.text.replace(before_str, after_str)
                    # 不存在
                    _ = self.repo.create_file(file_path, f"Add {file_msg}", content)

                LOGGER.info(f"Backup({self.backup_type}): {file_path} 上传成功！")
                # 保存当前文章状态
                self.save_backup(
                    doc_source=doc_source,
                    doc_source_name=doc_source_name,
                    doc_name=doc_name,
                )
            except GithubException as e:
                LOGGER.error(f"Backup({self.backup_type}): {file_path} 上传失败！{e}")
        else:
            LOGGER.info(f"Backup({self.backup_type}): {file_path} 已存在！")

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
        contents = self.repo.get_contents(file_path)

        try:
            _ = self.repo.delete_file(
                contents.path, f"Remove {file_path}", contents.sha
            )
            LOGGER.info(f"Backup({self.backup_type}): {file_path} 删除成功！")
            # 删除当前文章状态
            self.delete_backup(
                doc_source=doc_source,
                doc_source_name=doc_source_name,
                doc_name=doc_name,
            )
        except Exception as e:
            LOGGER.error(f"Backup({self.backup_type}): {file_path} 删除失败！{e}")


if __name__ == "__main__":
    test_backup_data = {
        "doc_id": "test",
        "doc_source": "liuli_wechat",
        "doc_source_name": "老胡的储物柜",
        "doc_name": "打造一个干净且个性化的公众号阅读环境",
        "doc_link": "https://mp.weixin.qq.com/s/NKnTiLixjB9h8fSd7Gq8lw",
    }
    github_backup = GithubBackup({})
    github_backup.save(test_backup_data)
    github_backup.delete(
        doc_source="liuli_wechat",
        doc_source_name="老胡的储物柜",
        doc_name="打造一个干净且个性化的公众号阅读环境",
    )
