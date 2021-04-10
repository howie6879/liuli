#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：HTTP API 服务
    Changelog: all notable changes to this file will be documented
"""

from flask import Flask

from src.api.views import bp_api
from src.config import Config
from src.databases import MongodbManager


def create_app():
    """
    建立web应用
    url: http://flask.pocoo.org/docs/1.0/quickstart/
    :return:
    """
    flask_app = Flask(__name__)

    with flask_app.app_context():
        # 项目内部配置
        mongodb_base = MongodbManager.get_mongo_base(
            mongodb_config=Config.MONGODB_CONFIG
        )

        flask_app.config["app_config"] = Config
        flask_app.config["mongodb_base"] = mongodb_base

    flask_app.register_blueprint(bp_api)
    return flask_app


app = create_app()


if __name__ == "__main__":
    # pipenv run gunicorn -c src/config/gunicorn.py src.api.http_app:app
    app.run(host=Config.HOST, port=Config.HTTP_PORT, debug=Config.DEBUG)
