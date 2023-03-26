"""
    Created by howie.hu at 2023-03-26.
    Description: Flask 蓝图
    Changelog: all notable changes to this file will be documented
"""
import os

from importlib import import_module

from flask import Blueprint

from src.config import API_LOGGER, Config

bp_api = Blueprint("bp_api", __name__)


def add_route(api_path: str):
    """
    增加路由
    Args:
        api_path (str): 路由函数名称
    """

    if "__" not in api_path and api_path.endswith("py"):
        try:
            api_path = api_path.replace(".py", "")
            route_path = api_path.split("views")[-1]
            module_path = api_path.split("src")[-1].replace("/", ".")
            view_func = api_path.split("views/api/")[-1].replace("/", "_")
            action_module = import_module(f"src{module_path}")
            bp_api.add_url_rule(
                route_path,
                view_func=getattr(action_module, view_func),
                methods=["POST", "GET"],
            )
        except Exception as e:
            API_LOGGER.error(f"Adding the route {route_path} in Flask has failed. {e}")


for each_action in os.listdir(Config.API_ACTION_DIR):
    action_path = full_path = os.path.join(Config.API_ACTION_DIR, each_action)
    if os.path.isdir(full_path):
        for each_dir_action in os.listdir(full_path):
            action_path = os.path.join(full_path, each_dir_action)
            add_route(action_path)

    else:
        add_route(action_path)
