#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/25.
    Description：
    Changelog: all notable changes to this file will be documented
"""

import os

from keras.optimizers import SGD


class Config:
    """
    模型基本配置
    """

    base_dir = os.path.dirname(os.path.dirname(__file__))
    # 字母表
    alphabet = """i（,l）h《$9a～“g」”』~.?j7·x)—;}'》k`|&>rvf5*0q：de{/":？w3，_ys#｜^8-『】[41%!<「bn+(om…6【tp=！c@uz]\2"""
    alphabet_size = len(alphabet)
    # 输入大小，即论文中的l0
    input_size = 128
    # 训练集类别
    num_of_classes = 2

    # 批大小
    batch_size = 12
    # 迭代次数
    epochs = 20

    # 每多少次 checkpoint
    checkpoint_every = 100
    # 每个迭代周期里面每多少次batch计算一次 0 表示不计算
    evaluate_every = 200

    # 激活函数的 threshold 值
    threshold = 1e-6
    # 防止过拟合
    dropout_p = 0.5

    # 卷积层配置
    conv_layers = [
        [256, 7, 3],
        [256, 7, 3],
        [256, 3, None],
        [256, 3, None],
        [256, 3, None],
        [256, 3, 3],
    ]

    # 全连接层配置
    fully_layers = [1024, 1024]

    # Keras 参数配置
    sgd = SGD(lr=0.001)
    # 损失函数
    loss = "categorical_crossentropy"
    # 优化器 rmsprop adam
    optimizer = "adam"
    # Keras 日志输出配置
    verbose = 1
