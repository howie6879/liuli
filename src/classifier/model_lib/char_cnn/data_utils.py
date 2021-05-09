#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/25.
    Description：数据加载工具类，参考：https://github.com/mhjabreel/CharCNN 感谢
    Changelog: all notable changes to this file will be documented
"""

import numpy as np
import pandas as pd


class DataUtils:
    """
    此类用于加载原始数据
    """

    def __init__(
        self,
        data_source: str,
        *,
        alphabet: str = """i（,l）h《$9a～“g」”』~.?j7·x)—;}'》k`|&>rvf5*0q：de{/":？w3，_ys#｜^8-『】[41%!<「bn+(om…6【tp=！c@uz]\2""",
        batch_size=128,
        input_size: int = 1014,
        num_of_classes: int = 2
    ):
        """
        数据初始化
        :param data_source: 原始数据路径
        :param alphabet: 索引字母表
        :param input_size: 输入特征 相当于论文中说的l0
        :param num_of_classes: 据类别
        """

        self.alphabet = alphabet
        self.alphabet_size = len(self.alphabet)
        self.batch_size = batch_size
        self.data_source = data_source
        self.length = input_size
        self.num_of_classes = num_of_classes

        # 将每个字符映射成int
        self.char_dict = {}
        self.data = np.array([])
        for idx, char in enumerate(self.alphabet):
            self.char_dict[char] = idx + 1

    @property
    def data_length(self):
        """
        返回数据集长度
        :return:
        """
        return len(self.data)

    def get_all_data(self):
        """
        返回全部数据
        """
        data_size = self.data_length
        start_index = 0
        end_index = data_size
        batch_texts = self.data[start_index:end_index]
        batch_indices = []
        one_hot = np.eye(self.num_of_classes, dtype="int64")
        classes = []
        for c, s in batch_texts:
            batch_indices.append(self.str_to_indexes(s))
            c = int(c) - 1
            classes.append(one_hot[c])
        return np.asarray(batch_indices, dtype="int64"), np.asarray(classes)

    def get_batch_to_indices(self, batch_num=0):
        """
        返回随机样本
        :param batch_num: 每次随机分配的样本数目
        :return: (data, classes)
        """
        data_size = len(self.data)
        start_index = batch_num * self.batch_size
        # 最长不超过数据集本身大小
        end_index = (
            data_size
            if self.batch_size == 0
            else min((batch_num + 1) * self.batch_size, data_size)
        )
        batch_texts = self.shuffled_data[start_index:end_index]
        # 类别 one hot 编码
        one_hot = np.eye(self.num_of_classes, dtype="int64")

        batch_indices, classes = [], []
        for c, s in batch_texts:
            batch_indices.append(self.str_to_indexes(s))
            # 类别数字减一就是 one hot 编码的index
            classes.append(one_hot[int(c) - 1])

        return np.asarray(batch_indices, dtype="int64"), classes

    def load_data(self):
        """
        从文件加载原始数据
        Returns: None
        """
        data_df = pd.read_csv(self.data_source)
        self.data = data_df[["label", "text"]].values
        self.shuffled_data = self.data
        print("Data loaded from " + self.data_source)

    def shuffle_data(self):
        """
        将数据集打乱
        :return:
        """
        data_size = len(self.data)
        shuffle_indices = np.random.permutation(np.arange(data_size))
        self.shuffled_data = self.data[shuffle_indices]

    def str_to_indexes(self, s):
        """
        根据字符字典对数据进行转化
        :param s: 即将转化的字符
        :return: numpy.ndarray 长度为：self.length
        """
        # 论文中表明 对于比较大的数据可以考虑不用区分大小写
        s = s.lower()
        # 最大长度不超过 input_size 此处为 1014
        max_length = min(len(s), self.length)
        # 初始化数组
        str2idx = np.zeros(self.length, dtype="int64")
        for i in range(1, max_length + 1):
            # 逆序映射
            c = s[-i]
            if c in self.char_dict:
                str2idx[i - 1] = self.char_dict[c]
        return str2idx


if __name__ == "__main__":
    train_data_ins = DataUtils(data_source="../datasets/ag_news_csv/train.csv")
    train_data_ins.load_data()

    test_data_ins = DataUtils(data_source="../datasets/ag_news_csv/test.csv")
    test_data_ins.load_data()

    training_inputs, training_labels = train_data_ins.get_all_data()
    test_inputs, test_labels = test_data_ins.get_all_data()
    print(len(training_inputs), training_inputs[0])
    print(training_inputs.shape, training_labels.shape)
    print(len(training_labels), training_labels[0])
    print(len(test_inputs), test_inputs[0])
    print(len(test_labels), test_labels[0])
    print(test_inputs.shape, test_labels.shape)
    exit()
    with open("test.vec", "w") as fo:
        for i in range(len(train_data_ins.data)):
            # 类别
            c = train_data_ins.data[i][0]
            # 文本
            txt = train_data_ins.data[i][1]
            # 生成向量
            vec = ",".join(map(str, train_data_ins.str_to_indexes(txt)))

            fo.write("{}\t{}\n".format(c, vec))
