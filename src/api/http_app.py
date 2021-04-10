#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：HTTP API 服务
    Changelog: all notable changes to this file will be documented
"""

import asyncio

from flask import Flask

from src.api.views import bp_api
from src.collector.wechat import run_wechat_name_spider
from src.config import Config
from src.databases import MongodbManager
from src.utils import LOGGER


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
        app_loop = asyncio.get_event_loop()
        flask_app.config["app_config"] = Config
        flask_app.config["app_logger"] = LOGGER
        flask_app.config["app_loop"] = app_loop
        flask_app.config["mongodb_base"] = mongodb_base

        # 每次启动先保证公众号名称爬虫运行成功
        # spider = run_wechat_name_spider(loop=app_loop)
        # if spider.success_counts == 1:
        #     # 爬虫运行成功
        #     LOGGER.info("Wechat spider started successfully :)")
        LOGGER.info("API started successfully :)")

    flask_app.register_blueprint(bp_api)
    return flask_app


app = create_app()


if __name__ == "__main__":
    # pipenv run gunicorn -c src/config/gunicorn.py src.api.http_app:app
    app.run(host=Config.HOST, port=Config.HTTP_PORT, debug=Config.DEBUG)
