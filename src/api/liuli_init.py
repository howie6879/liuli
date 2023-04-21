"""
    Created by howie.hu at 2023-04-21.
    Description: 初始化函数
    Changelog: all notable changes to this file will be documented
"""
import time

from flask import Flask

from src.config import API_LOGGER, Config, init_env_config
from src.databases import MongodbManager, mongodb_find, mongodb_update_data
from src.utils import gen_random_str, md5_encryption


def init_liuli_app(flask_app: Flask) -> Flask:
    """
    初始化 liuli 项目状态
    """

    # 对数据库进行初始化
    ll_env_config = init_env_config()
    ll_db_config = ll_env_config["mongodb"]
    username = ll_env_config["username"]

    if ll_db_config:
        # 已经初始化，配置数据库
        Config.LL_MONGODB_CONFIG = ll_db_config
        mongodb_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        # 验证用户是否存在
        ll_user_coll = mongodb_base.get_collection(coll_name="liuli_user")
        ll_user_res = mongodb_find(
            ll_user_coll, {"username": username}, {"password": 0}
        )
        is_check_user = False
        if ll_user_res["status"]:
            ll_user_data = ll_user_res["info"][0] if ll_user_res["info"] else []
            if ll_user_data:
                # 用户已存在
                is_check_user = True
                API_LOGGER.info(f"初始化：查找用户 {username} 成功！")
            else:
                # 用户未初始化，直接进行默认初始化，默认用户名密码都为 liuli
                l_user_update_res = mongodb_update_data(
                    ll_user_coll,
                    {"username": username},
                    {
                        "$set": {
                            "username": username,
                            "password": md5_encryption("liuli"),
                            "updated_at": int(time.time()),
                        }
                    },
                )
                if l_user_update_res["status"]:
                    # 初始化成功
                    is_check_user = True
                    API_LOGGER.info(f"初始化：创建用户名密码成功！用户名密码为：{username}:liuli")
                else:
                    API_LOGGER.error(
                        f"初始化：创建用户失败，请检查数据库配置: {l_user_update_res['info']}"
                    )
        if is_check_user:
            # 检查基本配置
            ll_config_coll = mongodb_base.get_collection(coll_name="liuli_config")
            ll_config_res = mongodb_find(ll_config_coll, {"config_flag": username}, {})
            if ll_config_res["status"]:
                config_data = ll_config_res["info"][0] if ll_config_res["info"] else {}
                # 判断必要key是否存在
                for each in ["LL_X_TOKEN", "LL_JWT_SECRET_KEY"]:
                    if not config_data.get(each, ""):
                        config_data[each] = md5_encryption(gen_random_str(32))
                        API_LOGGER.info(f"初始化：HTTP 配置 {each} 初始化成功")
                update_db_res = mongodb_update_data(
                    ll_config_coll,
                    {"config_flag": username},
                    {"$set": config_data},
                )

                if update_db_res["status"]:
                    # 初始化成功
                    Config.set_config(config_data)
                    flask_app.config["mongodb_base"] = mongodb_base
                    # 配置全局状态
                    flask_app.config["app_config"] = Config
                    flask_app.config["app_logger"] = API_LOGGER
                    return flask_app
                else:
                    API_LOGGER.error(f"初始化：更新用户配置失败， 检查数据库配置: {update_db_res['info']}")
                    exit()

            else:
                API_LOGGER.error(f"初始化：查找用户配置失败， 检查数据库配置: {ll_config_res['info']}")
                exit()
        else:
            API_LOGGER.error(f"初始化：查找用户配置失败， 检查数据库配置: {update_db_res['info']}")
            exit()

    API_LOGGER.info("初始化：检测到数据库未配置！")
    exit()
