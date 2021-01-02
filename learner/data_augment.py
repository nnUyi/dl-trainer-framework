# -*- coding:utf-8 -*-
# data_augment.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-24 23:44
# Distributed under term of Myself

import random
import numpy as np

from base.base_augment import BaseAugment

class DataAugment(BaseAugment):
    '''
        数据增强
    '''
    def __init__(self, config):
        BaseAugment.__init__(self, config)

    def data_augment(self, sample, label):
        sample, label = self._crop(sample, label)

        if self.config.DataAugmentConfig["to_tensor"]:
            sample, label = np.expand_dims(sample, axis=0), np.expand_dims(label, axis=0)
        return sample, label

    def _crop(self, sample, label):
        sample_shape = sample.shape
        label_shape = label.shape

        # 彩色图像:3通道
        is_color = len(sample_shape) == 3
          
        if sample_shape != label_shape:
            raise Exception("invalid sample_shape: {} and label_shape: {}".format(sample_shape, label_shape)) 

        sample_h, sample_w = sample_shape[0], sample_shape[1]
        label_h, label_w = label_shape[0], label_shape[1]

        crop_h, crop_w = self.config.DataAugmentConfig["crop_shape"]

        assert sample_h-crop_h > 0 and sample_w-crop_w > 0

        start_h_pos = random.randint(1, sample_h-crop_h)
        start_w_pos = random.randint(1, sample_w-crop_w)
        if is_color:
            crop_sample = sample[start_h_pos:start_h_pos+crop_h, start_w_pos:start_w_pos+crop_w, :]
            crop_label = label[start_h_pos:start_h_pos+crop_h, start_w_pos:start_w_pos+crop_w, :]
        else:
            crop_sample = sample[start_h_pos:start_h_pos+crop_h, start_w_pos:start_w_pos+crop_w]
            crop_label = label[start_h_pos:start_h_pos+crop_h, start_w_pos:start_w_pos+crop_w]

        return crop_sample, crop_label


if __name__ == "__main__":
    from config.config import Config
    import cv2
    from glob import glob

    import numpy as np   
 
    train_label_str = glob(Config.DataLoaderConfig["train_sample_str_input"])

    data_augmenter = DataAugment(Config) 

    for img_str in train_label_str:
        img = cv2.imread(img_str, 0)
        sample, label = data_augmenter.data_augment(img, img)
        sample_tensor, label_tensor = np.concatenate([np.expand_dims(sample, axis=0), np.expand_dims(sample, axis=0)], axis=0), np.concatenate([label], axis=0)
        print(sample_tensor.shape, label_tensor.shape)
        print(img_str, sample.shape, label.shape) 
