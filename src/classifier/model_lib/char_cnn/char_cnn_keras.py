#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/25.
    Description：模型实现
    Changelog: all notable changes to this file will be documented
"""


from keras import layers
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.models import Sequential

from src.classifier.model_lib.char_cnn.keras_utils import FitCallback


class CharCNN:
    def __init__(
        self,
        *,
        conv_layers: list = None,
        fully_layers: list = None,
        input_size: int = 1014,
        alphabet_size: int = 69,
        num_of_classes: int = 4,
        dropout_p: float = 0.5,
        threshold: float = 1e-6,
        loss="categorical_crossentropy",
        optimizer="adam",
    ):
        """
        基于Keras的字符级卷积神经网络
        :param conv_layers: 卷积层
        :param fully_layers: 全连接层
        :param input_size: 输入大小，论文中是1014
        :param alphabet_size: 字母表大小
        :param num_of_classes: 类别
        :param dropout_p: dropout值
        :param threshold: threshold值
        :param loss: 损失函数
        :param optimizer: 优化
        """
        # 卷积层定义
        if conv_layers is None:
            self.conv_layers = [
                [256, 7, 3],
                [256, 7, 3],
                [256, 3, None],
                [256, 3, None],
                [256, 3, None],
                [256, 3, 3],
            ]
        else:
            self.conv_layers = conv_layers
        # 全连接层
        if fully_layers is None:
            self.fully_layers = [1024, 1024]
        else:
            self.fully_layers = fully_layers

        self.alphabet_size = alphabet_size
        self.input_size = input_size
        self.num_of_classes = num_of_classes
        self.dropout_p = dropout_p
        self.threshold = threshold
        self.loss = loss
        self.optimizer = optimizer

        self.shape = (input_size, alphabet_size, 1)
        self.model = self._build_model()

    def _build_model(self):
        """
        论文中的模型结构
        :return:
        """
        model = Sequential()

        # 词嵌入
        model.add(
            layers.Embedding(self.alphabet_size + 1, 128, input_length=self.input_size)
        )
        # 卷积层
        for cl in self.conv_layers:
            model.add(layers.Conv1D(filters=cl[0], kernel_size=cl[1]))
            model.add(layers.ThresholdedReLU(self.threshold))
            if cl[-1] is not None:
                model.add(layers.MaxPool1D(pool_size=cl[-1]))

        model.add(layers.Flatten())
        # 全连接层
        for fl in self.fully_layers:
            # model.add(layers.Dense(fl, activity_regularizer=regularizers.l2(0.01)))
            model.add(layers.Dense(fl))
            model.add(layers.ThresholdedReLU(self.threshold))
            model.add(layers.Dropout(self.dropout_p))
        # 输出层
        model.add(layers.Dense(self.num_of_classes, activation="softmax"))

        model.compile(optimizer=self.optimizer, loss=self.loss, metrics=["accuracy"])
        print("CharCNN model built success")
        model.summary()
        return model

    def train(
        self,
        *,
        training_inputs,
        training_labels,
        validation_inputs,
        validation_labels,
        epochs,
        batch_size,
        model_file_path,
        verbose=2,
        checkpoint_every=100,
        evaluate_every=100,
    ):
        """
        对模型进项训练
        :param training_inputs: 训练实例
        :param training_labels: 训练标签
        :param validation_inputs: 验证实例
        :param validation_labels: 验证标签
        :param epochs:  迭代周期
        :param batch_size: 每次批大小
        :param model_file_path：模型保存路径
        :param verbose: Integer. 0, 1, or 2. Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch.
        :param checkpoint_every: 每多少次进行 checkpoint
        :param evaluate_every: 每多少次进行 evaluate
        :return:
        """

        tensorboard = TensorBoard(
            log_dir="./logs",
            histogram_freq=checkpoint_every,
            batch_size=batch_size,
            write_graph=True,
            write_grads=True,
            write_images=True,
            embeddings_freq=0,
            embeddings_layer_names=None,
        )
        fit_callback = FitCallback(
            test_data=(validation_inputs, validation_labels),
            evaluate_every=evaluate_every,
        )
        checkpoint = ModelCheckpoint(
            model_file_path,
            monitor="val_loss",
            verbose=1,
            save_best_only=True,
            mode="min",
        )

        # 开始训练
        print("Training Started ===>")
        self.model.fit(
            training_inputs,
            training_labels,
            validation_data=(validation_inputs, validation_labels),
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose,
            callbacks=[tensorboard, fit_callback, checkpoint],
        )


if __name__ == "__main__":
    char_cnn_model = CharCNN()
