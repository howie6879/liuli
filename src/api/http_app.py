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
from src.databases import MongodbManager


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
        flask_app.config["mongodb_base"] = mongodb_base
        # 配置全局状态
        flask_app.config["app_config"] = Config
        flask_app.config["app_logger"] = API_LOGGER

        return flask_app

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
