#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：余弦相似度
    Changelog: all notable changes to this file will be documented
"""

from functools import reduce
from math import sqrt

import numpy as np

np.seterr(divide="ignore", invalid="ignore")


class CosineSimilarity:
    """
    余弦相似性计算相似度
    """

    def __init__(self, init_query, target_data):
        """
        初始化相似度计算类
        :param init_query: 输入文本分词后向量
        :param target_data: 对比文本以及文本向量构成的字典 key 分别为index 以及value
        """
        self.init_query = init_query
        self.target_data = target_data
        self.word_vector = self.create_vector()

    def create_vector(self):
        """
        创建兴趣向量
        :return: word_vector = {} 文本以及文本向量 index: value 例如：[[1, 2, 1, 1, 2, 0, 1], [1, 2, 1, 2, 2, 1, 1]]
        """
        index, value = self.target_data["index"], self.target_data["value"]
        word_vector = {"index": index, "value": []}
        title_vector, value_vector = [], []
        all_word = set(self.init_query + value)
        for each_Word in all_word:
            title_num = self.init_query.count(each_Word)
            value_num = value.count(each_Word)
            title_vector.append(title_num)
            value_vector.append(value_num)
        word_vector["value"].append(title_vector)
        word_vector["value"].append(value_vector)
        return word_vector

    def calculate(self):
        """
        计算余弦相似度
        :param word_vector: word_vector = {} 文本以及文本向量 key 分别为index 以及value
        :return: 返回各个用户相似度值
        """
        result_dic = {}
        value = self.word_vector["value"]

        value_arr = np.array(value)
        # 余弦相似性
        squares = []
        numerator = reduce(lambda x, y: x + y, value_arr[0] * value_arr[1])
        square_title, square_data = 0.0, 0.0
        for num in range(len(value_arr[0])):
            square_title += pow(value_arr[0][num], 2)
            square_data += pow(value_arr[1][num], 2)
        squares.append(sqrt(square_title))
        squares.append(sqrt(square_data))
        mul_of_squares = reduce(lambda x, y: x * y, squares)
        value = float(("%.5f" % (numerator / mul_of_squares)))
        result_dic["index"] = self.word_vector["index"]
        result_dic["value"] = value
        return result_dic
