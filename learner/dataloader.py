# -*- coding:utf-8 -*-
# dataloader.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2020-11-17 23:04
# Distributed under term of Myself

import time
import cv2
import random
import logging
import multiprocessing as mp
import numpy as np

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from glob import glob
from base.base_dataloader import BaseDataLoader
from data_augment import DataAugment

logger = logging.getLogger(__name__)

class DataLoader(BaseDataLoader):
    def __init__(self, config, mode="train"):
        BaseDataLoader.__init__(self, config)

        assert mode in {"train", "test", "valid"}

        self.mode = mode
        self.data_queue = None
        self._stop_event = None
        self._threads = []

        # 训练过程做数据预处理        
        if self.mode == "train":
            self.data_augment = DataAugment(config)

        self.sample_worker_num = self.config.DataLoaderConfig["{}_worker_num".format(self.mode)]

    def start(self):
        def get_batch_data():
            while not self._stop_event.is_set():
                if self.data_queue.qsize() < self.config.DataLoaderConfig["max_queue_size"]:
                    batch_data = next(self.generator)
                    self.data_queue.put(batch_data)
                else:
                    time.sleep(self.config.DataLoaderConfig["sleep_time"])

        self.data_queue = mp.Queue(self.config.DataLoaderConfig["max_queue_size"])
        self._stop_event = mp.Event()

        # batch_data_generator_v1: 多进程队列写,单进程数据读
        # self.generator = self.batch_data_generator_v1()
        # batch_data_generator_v2: 多进程队列写,多进程数据读
        self.generator = self.batch_data_generator_v2()

        for idx in range(self.sample_worker_num):
            thread = mp.Process(target=get_batch_data)
            thread.daemon = True
            self._threads.append(thread)
            thread.start()
 
    def is_running(self):
        return (self._stop_event is not None) and (not self._stop_event.is_set())

    def stop(self):
        if self.is_running():
            self._stop_event.set() 

        for thread in self._threads:
            if thread.is_alive():
                thread.terminate()

        if self.data_queue is not None:
            self.data_queue.close()
         
        self.data_queue = None
        self._stop_event = None
        self._threads = []
 
    def batch_data_generator_v1(self):
        samples, labels = [], []
        single_data_generator = self.get_data()
        while not self._stop_event.is_set():
            sample, label = next(single_data_generator)

            # 训练过程处理数据
            if self.mode == "train":
                sample, label = self.data_augment.data_augment(sample, label)

            samples.append(sample)
            labels.append(label)
            if len(samples) == len(labels) and len(samples) == self.config.ModelConfig["batch_size"]:
                yield samples, labels
                samples, labels = [], []

    def batch_data_generator_v2(self):
        sample_str_input = glob(self.config.DataLoaderConfig["{}_sample_str_input".format(self.mode)])
        label_str_input = glob(self.config.DataLoaderConfig["{}_label_str_input".format(self.mode)])

        cpu_num = mp.cpu_count()
        max_workers = int(cpu_num / self.config.DataLoaderConfig["{}_worker_num".format(self.mode)])
        if not max_workers:
            max_workers = 1
            logger.warning("[MULTI-THREAD] thread pool executor max_works for reader is {}".format(max_workers))

        print("[MULTI-THREAD] data reader worker num: {}".format(max_workers))
        # 创建reader线程池
        thread_pool = ThreadPoolExecutor(max_workers=max_workers)

        while not self._stop_event.is_set():
            np.random.seed(random.randint(0, self.config.DataLoaderConfig["rand_seed"]))
            rand_state = np.random.get_state()
            np.random.shuffle(sample_str_input)
            np.random.set_state(rand_state)
            np.random.shuffle(label_str_input)

            samples, labels = [], []
            threads = []

            # 取随机打乱的数据list的前batch_size个
            for idx in range(self.config.ModelConfig["batch_size"]):
                sample_str = sample_str_input[idx]
                label_str = label_str_input[idx]
                threads.append(thread_pool.submit(self.read_pair_data, sample_str, label_str))

            for thread in as_completed(threads):
                sample, label = thread.result()
                if self.mode == "train":
                    sample, label = self.data_augment.data_augment(sample, label)
                samples.append(sample)
                labels.append(label)

            yield samples, labels

    def get_data(self):
        '''
            读取数据
        '''
        sample_str_input = glob(self.config.DataLoaderConfig["{}_sample_str_input".format(self.mode)])
        label_str_input = glob(self.config.DataLoaderConfig["{}_label_str_input".format(self.mode)])

        while not self._stop_event.is_set():
            # 相同顺序shuffle不同list
            np.random.seed(random.randint(0, self.config.DataLoaderConfig["rand_seed"]))
            rand_state = np.random.get_state()
            np.random.shuffle(sample_str_input)
            np.random.set_state(rand_state)
            np.random.shuffle(label_str_input)
            for sample_input, label_input in zip(sample_str_input, label_str_input):
                sample = self.read_single_data(sample_input)
                label = self.read_single_data(label_input)
                yield sample, label

    def read_single_data(self, str_input, dtype="img"):
        '''
            读取单个数据
        '''
        if dtype == "img":
            img = cv2.imread(str_input)
            return img
        else:
            raise Exception("invalid data dtype: {}".format(dtype))

    def read_pair_data(self, sample_str, label_str, dtype="img"):
        '''
            读取sample, label配对数据
        '''
        if dtype == "img":
            return cv2.imread(sample_str), cv2.imread(label_str)
        else:
            raise Exception("invalid data dtype: {}".format(dtype))
 
if __name__ == "__main__":
    from config.config import Config
    import time

    ite_num = 100
    train_dataloader = DataLoader(Config)
    print("train_dataloader is_running: {}".format(train_dataloader.is_running()))
    train_dataloader.start()
    print("train_dataloader is_running: {}".format(train_dataloader.is_running()))
    st = time.time()
    for idx in range(ite_num):
        i_st = time.time()
        samples, labels = train_dataloader.data_queue.get()
        print("samples len:{}, sample_shape:{}".format(len(samples), samples[0].shape))
        i_et = time.time()
        print("per cost time: {}".format(i_et-i_st))
    et = time.time()
    print("cost time: {}".format(et-st))
    print("train_dataloader is_running: {}".format(train_dataloader.is_running()))
    # stop dataloader
    train_dataloader.stop()
    print("train_dataloader is_running: {}".format(train_dataloader.is_running()))
