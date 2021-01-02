# -*- coding:utf-8 -*-
# algorithm.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import tensorflow as tf
from model import Model

class Algorithm(object):
    '''
        algorithm: 实现build_graph,构建网络模型,设计损失函数,计算精度
    '''

    def __init__(self, config):
        self.model = Model(config)
        self.config = config
        
    def build_graph(self, feature, label):
        predict_label = self.model.inference(feature)
        loss = tf.losses.mean_squared_error(label, predict_label)
        # correct_predict = tf.equal(tf.argmax(predict_label, axis=1), tf.argmax(label, axis=1))
        # accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))
        accuracy = None
        return loss, [accuracy]
    
    def get_optimizer(self):
        optim = tf.train.AdamOptimizer(learning_rate=self.config.OptimConfig["lr"], beta1=self.config.OptimConfig["beta1"], beta2=self.config.OptimConfig["beta2"])
        return optim
