#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/10.
    Description：对订阅的文章进行广告标记，调度与文章更新后
    Changelog: all notable changes to this file will be documented
"""

from src.classifier import model_predict_factory
from src.config import Config
from src.databases import MongodbManager


def ads_tag_update():
    """
    对订阅的文章进行广告标记
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="2c_articles")
    # 查找没有被标记的文章，基于预先相似度模型进行判断
    for each_data in coll.find({"cos_model": {"$exists": False}}):
        doc_name = each_data["doc_name"]
        # 基于余弦相似度
        cos_model_resp = model_predict_factory(
            model_name="cos",
            model_path="",
            input_dict={"text": doc_name, "cos_value": 0.65},
        ).to_dict()
        each_data["cos_model"] = cos_model_resp
        if cos_model_resp["result"] == 1:
            print(
                f"{doc_name} 被识别为广告[{cos_model_resp['probability']}]，链接为：{each_data['doc_link']}"
            )
        coll.update_one(
            filter={"doc_id": each_data["doc_id"]},
            update={"$set": each_data},
            upsert=True,
        )


if __name__ == "__main__":
    ads_tag_update()
