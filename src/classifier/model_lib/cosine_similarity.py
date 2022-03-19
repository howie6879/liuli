#!/usr/bin/env python
"""
    Created by howie.hu at 2021-04-08.
    Description：余弦相似度
    Changelog: all notable changes to this file will be documented
"""

from functools import reduce
from math import sqrt


class CosineSimilarity:
    """
    余弦相似性计算相似度
    """

    def __init__(self, source_data, target_data):
        """
        初始化相似度计算类
        :param source_data: 输入向量
        :param target_data: 向量字典 分别为index 以及value
        """
        self.source_data = source_data
        self.target_data = target_data
        self.word_vector = self.create_vector()

    def create_vector(self) -> dict:
        """
        创建向量
        :return: word_vector = {} eg: {'s_vector': [0, 1, 1, 1], 't_vector': [1, 1, 0, 1]}
        """
        # index, value = self.target_data["index"], self.target_data["value"]

        s_vector, t_vector = [], []
        # 统计所有词
        all_word = set(self.source_data + self.target_data)
        # 计算词频
        for each_Word in all_word:
            s_num = self.source_data.count(each_Word)
            t_num = self.target_data.count(each_Word)
            s_vector.append(s_num)
            t_vector.append(t_num)

        word_vector = {"s_vector": s_vector, "t_vector": t_vector}
        return word_vector

    def calculate(self) -> float:
        """
        计算余弦相似度
        :param word_vector: word_vector = {}
        :return: 返回相似度值
        """
        z_value_list = list(
            zip(self.word_vector["s_vector"], self.word_vector["t_vector"])
        )
        # 两个列表各个点位相乘再累加
        numerator = reduce(lambda x, y: x + y, [x * y for x, y in z_value_list])
        square_s, square_t = 0.0, 0.0
        for x, y in z_value_list:
            square_s += pow(x, 2)
            square_t += pow(y, 2)

        mul_of_squares = sqrt(square_s) * sqrt(square_t)
        cos_pro = float(("%.5f" % (numerator / mul_of_squares)))
        return cos_pro


if __name__ == "__main__":
    cos_ins = CosineSimilarity(
        ["毕业", "4", "年", "我用", "睡", "后", "收入", "买", "两", "套房"],
        [
            "毕业",
            "4",
            "年",
            "我用",
            "睡",
            "后",
            "收入",
            "买",
            "两",
            "套房",
            "理财",
            "赚钱",
            "慧如",
            "实现",
            "收益",
            "人生",
            "收入",
            "存款",
            "能力",
            "不用",
            "例子",
            "工作",
            "学员",
            "基金",
            "通俗易懂",
            "工资",
            "年轻人",
            "月入",
            "拼得",
            "客户资料",
        ],
    )
    print(cos_ins.calculate())
