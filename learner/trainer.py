# -*- coding:utf-8 -*-
# trainer.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import time
import logging
import tensorflow as tf
import numpy as np

from algorithm import Algorithm
from dataloader import DataLoader

logger = logging.getLogger(__name__)

class Trainer(object):
    def __init__(self, config, sess):
        self.config = config
        self.sess = sess
        self.algorithm = Algorithm(config)

        # 获取训练和测试数据集
        self.train_dataloader = DataLoader(config, mode="train")
        self.test_dataloader = DataLoader(config, mode="test")

        # 输入输出shape
        self.input_shape = self.config.ModelConfig["input_shape"]
        self.output_shape = self.config.ModelConfig["output_shape"]
        self.input_shape.insert(0, None)
        self.output_shape.insert(0, None)

        self.feature = tf.placeholder(shape=self.input_shape, dtype=tf.float32, name="feature")
        self.label = tf.placeholder(shape=self.output_shape, dtype=tf.float32, name="label")
        self.loss, self.accuracy = self.algorithm.build_graph(self.feature, self.label)
        self.optim = self.algorithm.get_optimizer()
        # 构建训练节点
        self.train_op = self.optim.minimize(self.loss)

    def load_model(self):
        raise NotImplementedError("Trainer load_model not implement")

    def save_model(self):
        raise NotImplementedError("Trainer save_model not implement")

    def test(self):
        raise NotImplementedError("Trainer test not implement")

    def vaild(self):
        raise NotImplementedError("Trainer valid not implement")

    def train(self):
        '''
        logger.debug("train_dataloader is_running: {}".format(self.train_dataloader.is_running()))
        logger.debug("test_dataloader is_running: {}".format(self.test_dataloader.is_running()))
        self.train_dataloader.start()
        self.test_dataloader.start()
        logger.debug("train_dataloader is_running: {}".format(self.train_dataloader.is_running()))
        logger.debug("test_dataloader is_running: {}".format(self.test_dataloader.is_running()))
        import time
        time.sleep(100)
        self.train_dataloader.stop()
        self.test_dataloader.stop()
        '''
        # load训练数据集
        self.train_dataloader.start()
        # 初始化网络参数
        self.sess.run(tf.global_variables_initializer())

        while True:
            data_st = time.time()
            samples, labels = self.train_dataloader.data_queue.get()
            samples_tensor, labels_tensor = np.concatenate(samples, axis=0), np.concatenate(labels, axis=0)
            data_et = time.time()
            logger.info("dataloader time:{}".format(data_et-data_st))
            model_st = time.time()
            self.sess.run(self.train_op, {self.feature:samples_tensor, self.label:labels_tensor})
            model_et = time.time()
            logger.info("model inference time:{}".format(model_et-model_st))
