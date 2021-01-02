# -*- coding:utf-8 -*-
# base_model.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

from abc import abstractmethod

class BaseModel(object):
    
    def __init__(self, config):
        self.config = config
    
    @abstractmethod    
    def model(self, feature):
        raise NotImplementedError
