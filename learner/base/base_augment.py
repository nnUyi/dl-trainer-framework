# -*- coding:utf-8 -*-
# base_augment.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-24 23:44
# Distributed under term of Myself

from abc import abstractmethod

class BaseAugment(object):
    '''
        DataAugment基类
    '''
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def data_augment(self):
        pass
