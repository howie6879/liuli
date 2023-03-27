"""
    Created by howie.hu at 2021/4/10.
    Description：HTTP API 服务
        - 启动命令:
            - gunicorn: PIPENV_DOTENV_LOCATION=./dev.env pipenv run  gunicorn -c src/config/gunicorn.py src.api.http_app:app
            - flask: PIPENV_DOTENV_LOCATION=./dev.env pipenv run  python src/api/http_app.py
    Changelog: all notable changes to this file will be documented
"""

from flask import Flask
from flask_jwt_extended import JWTManager

from src.api.views import bp_api, bp_backup, bp_rss
from src.config import API_LOGGER, Config, init_db_config
from src.databases import MongodbManager, mongodb_find, mongodb_update_data
from src.utils import gen_random_str, md5_encryption


def init_liuli_app(flask_app: Flask) -> Flask:
    """
    初始化 liuli 项目状态
    """

    # 对数据库进行初始化
    ll_db_config = init_db_config()
    if ll_db_config:
        # 已经初始化，配置数据库
        Config.LL_MONGODB_CONFIG = ll_db_config
        mongodb_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.LL_MONGODB_CONFIG
        )
        # 验证数据库可用性
        coll = mongodb_base.get_collection(coll_name="liuli_config")
        db_res = mongodb_find(coll, {}, {})
        if db_res["status"]:
            config_data = db_res["info"][0] if db_res["info"] else {}
            # 判断必要key是否存在
            for each in ["LL_X_TOKEN", "LL_JWT_SECRET_KEY"]:
                if not config_data.get(each, ""):
                    config_data[each] = md5_encryption(gen_random_str(32))
                    API_LOGGER.info(f"HTTP 配置 {each} 初始化成功")
            # 数据唯一标识
            config_flag = config_data.get("config_flag", "liuli")
            update_db_res = mongodb_update_data(
                coll, {"config_flag": config_flag}, {"$set": config_data}
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
            API_LOGGER.info(
                f"Detected that mongodb is connect failed! {db_res['status']}"
            )

    API_LOGGER.info("Detected that mongodb is not configured!")
    exit()


def create_app():
    """
    建立web应用
    url: http://flask.pocoo.org/docs/1.0/quickstart/
    :return:
    """
    flask_app = Flask(__name__)

    with flask_app.app_context():
        # 项目内部配置
        flask_app = init_liuli_app(flask_app)
        flask_app.config["app_logger"].info(
            f"server({Config.VERSION}) started successfully :)"
        )

    # 注册相关蓝图
    flask_app.register_blueprint(bp_api)
    flask_app.register_blueprint(bp_rss)
    flask_app.register_blueprint(bp_backup)

    # 初始化JWT
    flask_app.config["JWT_SECRET_KEY"] = Config.LL_JWT_SECRET_KEY
    _ = JWTManager(flask_app)

    return flask_app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=Config.LL_HTTP_HOST, port=Config.LL_HTTP_PORT, debug=Config.LL_HTTP_DEBUG
    )
