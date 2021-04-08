#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：模型校验脚本
    Changelog: all notable changes to this file will be documented
"""
from src.classifier import model_predict_factory
from src.config import Config
from src.databases import MongodbManager

mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)

coll = mongo_base.get_collection(coll_name="2c_articles")
for each in coll.find({}):
    doc_name = each["doc_name"]
    model_resp = model_predict_factory(
        model_name="cos", model_path="", input_dict={"text": doc_name, "cos_value": 0.5}
    ).to_dict()
    if model_resp["result"] == 1:
        print(f"{doc_name} 被识别为广告[{model_resp['probability']}]，链接为：{each['doc_link']}")
