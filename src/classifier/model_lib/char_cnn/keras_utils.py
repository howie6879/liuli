#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/25.
    Description：keras 回调钩子
    Changelog: all notable changes to this file will be documented
"""

from keras.callbacks import Callback


class FitCallback(Callback):
    def __init__(self, *, test_data: tuple, evaluate_every: int = 100):
        super(FitCallback, self).__init__()
        if test_data is None:
            raise ValueError("test_data is expected")
        self.test_data = test_data
        self.evaluate_every = evaluate_every

    def on_batch_end(self, batch, logs={}):
        # 批量训练开始函数
        if self.evaluate_every > 0:
            if (int(batch) + 1) % self.evaluate_every == 0:
                x, y = self.test_data
                result = self.model.evaluate(x, y, verbose=0)
                print("\n")
                print(
                    f"Iter: {int(batch) + 1}, Val Loss: {result[0]}, Val Acc: {result[1]}"
                )

    def on_epoch_end(self, epoch, logs={}):
        # 每次迭代结束
        pass
