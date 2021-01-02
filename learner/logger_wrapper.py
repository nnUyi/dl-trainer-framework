# -*- coding:utf-8 -*-
# logger_wrapper.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-28 12:42
# Distributed under term of Myself

import os
import logging

from logging.handlers import RotatingFileHandler

class LogWrapper(object):
    '''
        日志模块
    '''
    def __init__(self, config):
        self.config = config

    def logger_config(self):
        format_str = self.config.LogConfig["format_str"] 
        log_level = self.config.LogConfig["log_level"]
        log_path = self.config.LogConfig["log_path"]

        if not log_path:
            logging.basicConfig(log_level=log_level, format=format_str)
        else:
            if not os.path.exists(os.path.dirname(log_path)):
                os.makedirs(os.path.dirname(log_path))

        logging.basicConfig(log_level=log_level, format=format_str)

        rotate_file_handler = RotatingFileHandler(filename=log_path,
                                                  maxBytes=self.config.LogConfig["max_bytes"],
                                                  backupCount=self.config.LogConfig["backup_count"])
        rotate_file_handler.setLevel(log_level)
        formatter = logging.Formatter(format_str)
        rotate_file_handler.setFormatter(formatter)

        if logging.root.handlers:
            logging.root.handlers = []

        logging.root.addHandler(rotate_file_handler)
