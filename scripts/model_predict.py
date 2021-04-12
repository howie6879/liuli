#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：模型校验脚本
    Changelog: all notable changes to this file will be documented
"""
import requests

from src.classifier import model_predict_factory
from src.config import Config
from src.databases import MongodbManager


def cos_pre(text: str, cos_value: int = 0.5):
    """
    余弦相似度预测
    :param text:
    :type text: str
    :param cos_value:
    :type cos_value: int
    """
    return model_predict_factory(
        model_name="cos", model_path="", input_dict={"text": text, "cos_value": 0.5}
    ).to_dict()


def test_mongo_doc():
    """
    测试数据库文本
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    # coll = mongo_base.get_collection(coll_name="2c_articles")
    coll = mongo_base.get_collection(coll_name="2c_wechat_datasets")
    for each in coll.find({}):
        doc_name = each["doc_name"]
        model_resp = cos_pre(text=doc_name)
        if model_resp["result"] == 1:
            print(
                f"{doc_name} 被识别为广告[{model_resp['probability']}]，链接为：{each['doc_link']}"
            )


if __name__ == "__main__":
    text = "普通人搞一百万有多难"
    res = cos_pre(text=text)
    print(res)
    # test_mongo_doc()
