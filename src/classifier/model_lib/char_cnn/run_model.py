#!/usr/bin/env python
"""
    Created by howie.hu at 2021/5/9.
    Description：训练分类模型
    Changelog: all notable changes to this file will be documented
"""
import os

import numpy as np

from keras.models import load_model
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

from src.classifier.model_lib.char_cnn.char_cnn_keras import CharCNN
from src.classifier.model_lib.char_cnn.config import Config as CharCNNConfig
from src.classifier.model_lib.char_cnn.data_utils import DataUtils
from src.config import Config


def gen_datasets():
    """
    生成训练测试集
    :return:
    """
    ads_path = os.path.join(Config.DS_DIR, "final_ads.csv")
    normal_path = os.path.join(Config.DS_DIR, "final_normal.csv")

    normal_data_ins = DataUtils(
        data_source=normal_path,
        alphabet=CharCNNConfig.alphabet,
        batch_size=CharCNNConfig.batch_size,
        input_size=CharCNNConfig.input_size,
        num_of_classes=CharCNNConfig.num_of_classes,
    )
    normal_data_ins.load_data()
    p_inputs, p_labels = normal_data_ins.get_all_data()

    ads_data_ins = DataUtils(
        data_source=ads_path,
        alphabet=CharCNNConfig.alphabet,
        batch_size=CharCNNConfig.batch_size,
        input_size=CharCNNConfig.input_size,
        num_of_classes=CharCNNConfig.num_of_classes,
    )
    ads_data_ins.load_data()
    n_inputs, n_labels = ads_data_ins.get_all_data()

    training_inputs = np.append(p_inputs, n_inputs, axis=0)
    training_labels = np.append(p_labels, n_labels, axis=0)

    shuffle_indices = np.random.permutation(np.arange(len(training_inputs)))
    training_inputs = training_inputs[shuffle_indices]
    training_labels = training_labels[shuffle_indices]

    return training_inputs, training_labels


def train_model():
    """
    训练模型
    :return:
    """
    # 获取打乱的训练测试样本
    training_inputs, training_labels = gen_datasets()
    char_cnn_model = CharCNN(
        conv_layers=CharCNNConfig.conv_layers,
        fully_layers=CharCNNConfig.fully_layers,
        input_size=CharCNNConfig.input_size,
        alphabet_size=CharCNNConfig.alphabet_size,
        num_of_classes=CharCNNConfig.num_of_classes,
        dropout_p=CharCNNConfig.dropout_p,
        threshold=CharCNNConfig.threshold,
        loss=CharCNNConfig.loss,
        optimizer=CharCNNConfig.optimizer,
    )
    # 训练集_验证集:测试集 8:2
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        training_inputs, training_labels, test_size=0.1, shuffle=True, random_state=0
    )
    # 训练验证集切分，总体7:2:1 比例切分
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_val, y_train_val, test_size=0.125, random_state=6
    )
    model_path = os.path.join(Config.BASE_DIR, "classifier/model_data/char_cnn/v1.0.h5")

    char_cnn_model.train(
        training_inputs=X_train,
        training_labels=y_train,
        validation_inputs=X_valid,
        validation_labels=y_valid,
        epochs=CharCNNConfig.epochs,
        batch_size=CharCNNConfig.batch_size,
        verbose=CharCNNConfig.verbose,
        model_file_path=model_path,
        checkpoint_every=CharCNNConfig.checkpoint_every,
        evaluate_every=CharCNNConfig.evaluate_every,
    )
    model = char_cnn_model.model
    # model.save(model_path)

    # 查看测试结果
    y_predict = model.predict(X_test)

    pred_label = np.argmax(y_predict, axis=1)
    true_label = np.argmax(y_test, axis=1)

    print(classification_report(true_label, pred_label))
    # tn, fp, fn, tp
    confusion_mat = confusion_matrix(true_label, pred_label)
    tn, fp, fn, tp = confusion_mat.ravel()
    print(tn, fp, fn, tp)
    print(f"模型召回率为{tn / (tn + fp)}")
    print(f"模型精确率为{tp / (tp + fp)}")

    print("ROC曲线====>")
    y_score = y_predict[:, 1]
    fpr, tpr, thresholds = roc_curve(true_label, y_score, pos_label=1)

    auc_value = roc_auc_score(true_label, y_score)
    print(f"AUC======>{auc_value}")


def valid():
    """
    测试模型
    :return:
    """
    model_path = os.path.join(Config.BASE_DIR, "classifier/model_data/char_cnn/v1.0.h5")
    model = load_model(model_path)
    print(model)


if __name__ == "__main__":
    train_model()
    # valid()
