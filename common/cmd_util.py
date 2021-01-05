# -*- coding:utf-8 -*-
# cmd_util.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2021-01-05 10:58
# Distributed under term of Myself

def arg_parser():
    """
    Create an empty argparse.ArgumentParser.
    """
    import argparse
    return argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter

def common_arg_parser():
    """
    Create an argparse.ArgumentParser for common.
    """
    parser = arg_parser()
    return parser

def trainer_arg_parser():
    """
    Create an argparse.ArgumentParser for trainer.
    """
    trainer_parser = common_arg_parser()
    trainer_parser.add_argument('--mode', default='train', type=str, help='training or testing')
    return trainer_parser
