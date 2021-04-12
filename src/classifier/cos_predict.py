#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/8.
    Description：余弦相似度模型预测模块
    Changelog: all notable changes to this file will be documented
"""

from src.classifier.model_base.base import ModelPredictBase, ModelResponse
from src.utils import is_contain_text


class CosPredictModel(ModelPredictBase):
    """
    余弦相似度模型预测类
    """

    def __init__(self, model_name: str, model_path: str, input_dict: dict):
        """
        初始化模型
        :param model_name: 可选，目前只有 cos
        :param model_path: 训练集路径
        :param input_dict: 使用者自定义的输入配置字典
        """
        super().__init__(model_name, model_path, input_dict)
        # 加载模型
        model_dict = self._load_model()
        self.model = model_dict["model"]
        self.black_list = model_dict.get("black_list", [])
        self.white_list = model_dict.get("white_list", [])

    def process(self, text):
        """
        黑白名单判断
        :param text:
        :return:
        """
        is_black = is_contain_text(text, self.black_list)
        is_white = is_contain_text(text, self.white_list)
        self.model_resp.feature_dict.update(
            {"is_black": is_black, "is_white": is_white, "text": text}
        )
        return is_black, is_white

    def predict(self) -> ModelResponse:
        """
        返回预测结果
        :return:
        """
        # 定义的必传参数
        text: dict = self.input_dict["text"]
        cos_value: dict = self.input_dict.pop("cos_value", 0.65)
        if text:
            is_black, is_white = self.process(text)

            if is_white:
                # 白名单优先
                self.model_resp.result = 0
                self.model_resp.probability = 0.0
                return self.model_resp

            elif is_black:
                self.model_resp.result = 1
                self.model_resp.probability = 1.0
                return self.model_resp

            else:
                model_res = self.model.predict(text=text, cos_value=cos_value)
                self.model_resp.result = model_res["result"]
                self.model_resp.probability = model_res["value"]
        return self.model_resp


def predict(model_name: str, model_path: str, input_dict: dict) -> ModelResponse:
    """
    预测函数
    :param model_name:
    :param model_path:
    :param input_dict:
    :return:
    """
    return CosPredictModel(model_name, model_path, input_dict).predict()
