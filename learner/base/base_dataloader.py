# -*- coding:utf-8 -*-
# base_dataloader.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-20 16:21
# Distributed under term of Myself

from abc import abstractmethod

class BaseDataLoader(object):
    '''
        DataLoader基类
    '''
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def start(self):
        raise NotImplementedError("DataLoader: start not implement")

    @abstractmethod
    def stop(self):
        raise NotImplementedError("DataLoader: stop not implement")

    @abstractmethod
    def is_running(self):
        raise NotImplementedError("DataLoader: is_running not implement")

    @abstractmethod
    def batch_data_generator(self):
        raise NotImplementedError("DataLoader: batch_data_generator not implement")

    @abstractmethod
    def get_data(self):
        raise NotImplementedError("DataLoader: get_data not implement")

    @abstractmethod
    def read_data(self, str_input, dtype="img"): 
        raise NotImplementedError("DataLoader: read_data not implement")
