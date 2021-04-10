#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：模型预测工厂
    Changelog: all notable changes to this file will be documented
"""
from importlib import import_module

from src.classifier.model_base.base import ModelResponse


def model_predict_factory(
    model_name: str, model_path: str, input_dict: dict
) -> ModelResponse:
    """
    模型预测工厂函数
    :param model_name:
    :param model_path:
    :param input_dict:
    :return:
    """
    try:
        predict_module = import_module(f"src.classifier.{model_name}_predict")
        model_response = predict_module.predict(model_name, model_path, input_dict)
    except ModuleNotFoundError:
        raise ValueError(f"模型不存在 {model_name} - {model_path}")
    return model_response


if __name__ == "__main__":
    model_response = model_predict_factory(
        model_name="cos", model_path="", input_dict={"text": "毕业的4年，我用睡后收入买了两套房"}
    )
    print(model_response.to_dict())
