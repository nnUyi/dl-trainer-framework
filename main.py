# -*- coding:utf-8 -*-
# main.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import tensorflow as tf

from learner.config.config import Config
from learner.trainer import Trainer
from learner.logger_wrapper import LogWrapper

from common.cmd_util import trainer_arg_parser

trainer_arg_parser = trainer_arg_parser()
args = trainer_arg_parser.parse_args()

def main(_):
    config = Config()
    # 全局配置日志
    LogWrapper(config).logger_config()    
    sess = tf.Session()
    trainer = Trainer(config, sess)
    if args.mode == "train":
        trainer.train()
    elif args.mode == "test":
        trainer.test()
    else:
        raise Exception("[MODEERROR] invalid mode: {}".format(args.mode))

if __name__ == "__main__":
    tf.app.run()
