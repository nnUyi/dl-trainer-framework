# -*- coding:utf-8 -*-
# config.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import os
import logging
# 获取根目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class Config(object):
    ModelConfig = {"input_shape": [None, None, 3],
                   "output_shape": [None, None, 3],
                   "batch_size": 64,
                   "n_channel": 32}
    OptimConfig = {"lr": 2e-4,
                   "beta1": 0.9,
                   "beta2": 0.999}
    DataLoaderConfig = {"max_queue_size": 128,
                        "sleep_time":0.5,
                        "rand_seed": 2**32 - 1,
                        "train_worker_num":4,
                        "test_worker_num": 4,
                        "valid_worker_num": 2,
                        "train_sample_str_input": os.path.join(BASE_DIR, "data/samples/*.png"),
                        "train_label_str_input": os.path.join(BASE_DIR, "data/labels/*.png"),
                        "test_sample_str_input": os.path.join(BASE_DIR, "data/samples/*.png"),
                        "test_label_str_input": os.path.join("data/labels/*.png")}

    DataAugmentConfig = {"to_tensor":True, "crop_shape": (64, 64)}
    LogConfig = {"format_str": "%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s",
                 "log_level": logging.INFO,
                 "log_path": os.path.join(BASE_DIR, "log/trainer.log"),
                 "stderr_log_path": os.path.join(BASE_DIR, "log/stderr.log"),
                 "max_bytes": 1024 * 1024 * 50,
                 "backup_count": 10}
