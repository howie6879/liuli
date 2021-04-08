#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：模型父类
    Changelog: all notable changes to this file will be documented
"""
from importlib import import_module


class ModelManager:
    """
    模型管理类
    """

    _model_load_dict = {}

    @classmethod
    def get_model(cls, model_name: str, model_path: str, **kwargs):
        """get_model.
        获取配置对应的模型
        :param model_name:
        :type model_name: str
        :param model_path:
        :type model_path: str
        :param kwargs:
        """
        model_key = f"{model_name}_{model_path}"
        if model_key not in cls._model_load_dict:
            model_loader = import_module(
                f"src.classifier.model_base.{model_name}_model_loader"
            )
            try:
                cls._model_load_dict[model_key] = model_loader.get_model(
                    model_path, **kwargs
                )
            except Exception as e:
                err_info = f"{model_name}: {model_path} 加载失败"
                raise ValueError(err_info)
        return cls._model_load_dict[model_key]


class ModelLoaderBase:
    """
    模型加载父类
    """

    def __init__(self, model_path: str, **kwargs):
        """
        属性初始化
        :param model_path:
        :type model_path: str
        :param kwargs:
        """
        self.model_path = model_path
        self.kwargs = kwargs

    def get_model(self) -> dict:
        """
        获取模型
        :return:
        """
        raise NotImplementedError()


class ModelResponse:
    """
    模型响应父类，定义一些常用属性
    """

    def __init__(self):
        """
        属性初始化
        """
        self.model_name = ""
        # 0 正常 1 异常
        self.result = 0
        self.probability = 0.0
        # 特征字典
        # 基础key有：
        # - is_black:   是否黑名单
        # - is_white:   是否白名单
        # - text:       输入文本
        self.feature_dict = {}

    def to_dict(self):
        """
        返回字典
        :return:
        """
        return {
            "model_name": self.model_name,
            "result": self.result,
            "probability": self.probability,
            "feature_dict": self.feature_dict,
        }


class ModelPredictBase:
    """
    模型父类，抽象流程
    """

    def __init__(self, model_name: str, model_path: str, input_dict: dict):
        """__init__.
        属性初始化
        :param model_name: 模型名称
        :type model_name: str
        :param model_path: 模型路径
        :type model_path: str
        :param input_dict: 输入配置
        :type input_dict: dict
        """
        self.model_name = model_name
        self.model_path = model_path
        self.input_dict = input_dict
        # 模型响应类
        self.model_resp: ModelResponse = ModelResponse()
        self.model_resp.model_name = model_name
        # 自定义返回内容
        self.model_resp.feature_dict = {}

    def _load_model(self):
        """
        加载模型
        """
        return ModelManager.get_model(self.model_name, self.model_path)

    def process(self, **kwargs):
        """
        模型开始预测时候可能需要的处理函数
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def predict(self):
        """
        模型预测函数，模型预测类的唯一入口
        :return:
        """
        raise NotImplementedError
