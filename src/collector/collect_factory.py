"""
    Created by howie.hu at 2022-01-05.
    Description: 采集器工厂函数，根据采集模块名称启动主函数
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/collect_factory.py
    Changelog: all notable changes to this file will be documented
"""

from importlib import import_module

from src.utils import LOGGER


def collect_factory(collect_type: str, collect_config: dict) -> bool:
    """
    采集器工厂函数
    :param collect_type: 采集器类型
    :param collect_config: 采集器配置
    :return:
    """
    collect_status = False
    try:
        collect_module = import_module(f"src.collector.{collect_type}")
        collect_status = collect_module.run(collect_config)
    except ModuleNotFoundError:
        LOGGER.error(f"采集器类型不存在 {collect_type} - {collect_config}")
    except Exception as e:
        LOGGER.error(f"采集器执行出错 {collect_type} - {collect_config} - {e}")
    return collect_status


if __name__ == "__main__":
    t_collect_type = "wechat_sougou"
    t_collect_config = {"wechat_list": ["老胡的储物柜"], "delta_time": 5}
    collect_factory(t_collect_type, t_collect_config)
