# -*- coding:utf-8 -*-
# model.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import tensorflow as tf
from base.base_model import BaseModel

class Model(BaseModel):
    '''
        model:实现inference的网络模型搭建
    '''
    def __init__(self, config):
        BaseModel.__init__(self, config)
 
    def inference(self, feature):
        with tf.variable_scope("feature_extractor") as fe_scope:
            rainy_feature = tf.layers.conv2d(feature, self.config.ModelConfig["n_channel"], 3, padding="same", activation=tf.nn.relu)
        with tf.variable_scope("feature_mapping") as fm_scope:
            layer1 = tf.layers.conv2d(rainy_feature, self.config.ModelConfig["n_channel"]*2, 3, padding="same", activation=tf.nn.relu)
            layer2 = tf.layers.conv2d(layer1, self.config.ModelConfig["n_channel"]*4, 3, padding="same", activation=tf.nn.relu)
            layer3 = tf.layers.conv2d(layer2, self.config.ModelConfig["n_channel"]*2, 3, padding="same", activation=tf.nn.relu)
            layer4 = tf.layers.conv2d(layer3, self.config.ModelConfig["n_channel"], 3, padding="same", activation=tf.nn.relu)
        with tf.variable_scope("rainy_map_generator") as rmg_scope:
            rainy_map = tf.layers.conv2d(layer4, self.config.ModelConfig["output_shape"][-1], 3, padding="same", activation=None)
        return rainy_map
