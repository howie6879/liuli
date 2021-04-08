#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：余弦相似度模型加载器
    Changelog: all notable changes to this file will be documented
"""
import os

import jieba

from src.classifier.model_base.base import ModelLoaderBase
from src.classifier.model_lib import CosineSimilarity
from src.config import Config
from src.utils import load_text_to_list


class CosModel(ModelLoaderBase):
    """
    余弦相似度模型
    """

    def __init__(self, model_path: str, **kwargs):
        """
        初始化
        :param model_path: 这里模型路径指的是训练文件路径
        :type model_path: str
        :param kwargs:
        """
        super().__init__(model_path, **kwargs)
        self.stop_word_path = os.path.join(Config.MODEL_DIR, "data/stop_words.txt")
        self.black_list_path = os.path.join(Config.MODEL_DIR, "data/black.txt")
        self.white_list_path = os.path.join(Config.MODEL_DIR, "data/white.txt")

        # 加载数据
        self.black_data: list = load_text_to_list(self.black_list_path)
        self.white_data: list = load_text_to_list(self.white_list_path)
        self.stop_word_data: list = load_text_to_list(self.stop_word_path)

        # 对训练数据进行预处理，形成最终可用样本
        self.train_data: list = [
            {"index": i, "value": self.process_text(i)}
            for i in load_text_to_list(model_path)
        ]

    def predict(self, text: str, cos_value: float = 0.9) -> dict:
        """
        对文本相似度进行预测
        :param text: 文本
        :param cos_value: 阈值 默认是0.9
        :return:
        """
        max_pro, result = 0.0, 0
        for each in self.train_data:
            cos = CosineSimilarity(self.process_text(text), each)
            res_dict = cos.calculate()
            value = res_dict["value"]
            result = 1 if value >= cos_value else 0
            max_pro = value if value > max_pro else max_pro
            if result == 1:
                break
        predict_dict = {"result": result, "value": max_pro}
        return predict_dict

    def process_text(self, text: str) -> list:
        """
        文本处理
        :param text:
        :return:
        """
        seg_list = []
        msg_list = jieba.cut(text)
        for each in msg_list:
            if each not in self.stop_word_data and not each.isspace():
                seg_list.append(str(each).strip().lower())
        return seg_list

    def get_model(self) -> dict:
        pass


if __name__ == "__main__":
    print(CosModel("").stop_word_path)
