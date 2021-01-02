# -*- coding:utf-8 -*-
# time_stat.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2021-01-01 16:05
# Distributed under term of Myself

import time
import datetime
import enum

"""
    说明：时间统计工具
    单位：毫秒
"""

@enum.unique
class TimeoutManager(enum.Enum):
    """
        超时设置基类，继承python3的enum新特性
    """
    # 单位为毫秒
    TIME_PHASE_1 = 500
    TIME_PHASE_2 = 1000
    TIME_PHASE_3 = 1500

    def __len__(self):
        return len(TimeoutManager.__members__)

class TypeInfo(object):
    """
        统计信息基类
    """
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.type_name = None
        self.failed_cnt = 0
        self.all_cnt = 0
        self.min_time = 0
        self.max_time = 0
        self.st_time = 0
        self.has_time = False
        self.time_out_lst_cnt = [0]*len(TimeoutManager)

    def __str__(self):
        return "{}|{}|{}|{}|{}|{}|{}|{}".format(self.type_name,
                                                self.failed_cnt,
                                                self.all_cnt,
                                                self.min_time,
                                                self.max_time,
                                                self.st_time,
                                                self.has_time,
                                                self.time_out_lst_cnt)

class CStatistic(object):
    """
        时间统计基类
    """

    def __init__(self):
        self.c_stat_name = "CStatistic"
        self.time_out_lst = [timeout.value for timeout in TimeoutManager]
        self.last_clear_time = time.time()
        self.stat_dict = dict()
    
    def add_stat(self, type_name, result_id, pst_begin, pst_end, stat_cnt):
        """
            时间统计
        """

        cur_stat = self.stat_dict.get(type_name)
        if cur_stat is None:
            self.stat_dict[type_name] = TypeInfo()
            cur_stat = self.stat_dict.get(type_name)
            cur_stat.type_name = type_name

        cur_stat.all_cnt += stat_cnt
        if result_id != 0:
            cur_stat.failed_cnt += stat_cnt

        self._add_time(cur_stat, pst_begin, pst_end)

    def _add_time(self, cur_stat, pst_begin, pst_end):
        if pst_begin is None or pst_end is None:
            cur_stat.has_time = False
            return
        
        cur_stat.has_time = True
        # 毫秒统计
        time_ms = (pst_end - pst_begin) * 10 ** 3
        if time_ms < 0:
            time_ms = 0.0
        if time_ms >= self.time_out_lst[0] and time_ms < self.time_out_lst[1]:
            cur_stat.time_out_lst_cnt[0] += 1
        elif time_ms >= self.time_out_lst[1] and time_ms < self.time_out_lst[2]:
            cur_stat.time_out_lst_cnt[1] += 1
        elif time_ms >= self.time_out_lst[2]:
            cur_stat.time_out_lst_cnt[2] += 1

        if time_ms > cur_stat.max_time:
            cur_stat.max_time = time_ms

        if cur_stat.min_time == 0 or time_ms < cur_stat.min_time:
            cur_stat.min_time = time_ms

        cur_stat.st_time += time_ms

    def get_stat_str(self, type_name, interval=60, process_end=False):
        """
            获取统计结果
        """

        # 判断时间适合符合统计间隔
        cur_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        diff_time = time.time() - self.last_clear_time
        if diff_time < interval or process_end:
            return None
        
        out_str = "\n======================================Statistic in %ds, %s==========================================\n" % (diff_time, cur_time_str)        

        sz_tmp_str1 = ">%.3fms" % (self.time_out_lst[0])
        sz_tmp_str2 = ">%.3fms" % (self.time_out_lst[1])
        sz_tmp_str3 = ">%.3fms" % (self.time_out_lst[2])
        out_str += "%-35s|%8s|%8s|%10s|%10s|%10s|%11s|%11s|%11s|\n" % (
            "", "TOTAL", "FAILED", "AVG(ms)", "MAX(ms)", "MIN(ms)",
            sz_tmp_str1, sz_tmp_str2, sz_tmp_str3)

        all_stat = TypeInfo()
        for _, cur_stat in self.stat_dict.items():
            print(str(cur_stat))
            tmp_avg_ms = 0
            if cur_stat.all_cnt > 0:
                tmp_avg_ms = cur_stat.st_time / cur_stat.all_cnt

            out_str += "%-35s|%8u|%8u|%10.2f|%10.2f|%10.2f|%11u|%11u|%11u|\n" % (
                cur_stat.type_name,
                cur_stat.all_cnt,
                cur_stat.failed_cnt,
                (tmp_avg_ms),
                (cur_stat.max_time),
                (cur_stat.min_time),
                cur_stat.time_out_lst_cnt[0],
                cur_stat.time_out_lst_cnt[1],
                cur_stat.time_out_lst_cnt[2])

            all_stat.all_cnt += cur_stat.all_cnt
            all_stat.failed_cnt = cur_stat.failed_cnt
            if all_stat.max_time < cur_stat.max_time:
                all_stat.max_time = cur_stat.max_time
            if all_stat.min_time == 0 or all_stat.min_time > cur_stat.min_time:
                all_stat.min_time = cur_stat.min_time

            all_stat.time_out_lst_cnt[0] += cur_stat.time_out_lst_cnt[0]
            all_stat.time_out_lst_cnt[1] += cur_stat.time_out_lst_cnt[1]
            all_stat.time_out_lst_cnt[2] += cur_stat.time_out_lst_cnt[2]

        out_str += "-"*123+"\n"
        out_str += "%-35s|%8u|%8u|%10.2f|%10.2f|%10.2f|%11u|%11u|%11u|\n" % (
            "ALL",
            all_stat.all_cnt,
            all_stat.failed_cnt,
            0.0,
            (all_stat.max_time),
            (all_stat.min_time),
            all_stat.time_out_lst_cnt[0],
            all_stat.time_out_lst_cnt[1],
            all_stat.time_out_lst_cnt[2])
        return out_str

    def clear(self):
        """
            清空统计项
        """
        self.last_clear_time = time.time()
        for _, val in self.stat_dict.items():
            val.reset()

g_stat = CStatistic()

class StatNode(object):
    """
        统计节点，辅助区间时间统计
    """
    def __init__(self, type_name):
        self.type_name = type_name
        self.begin_time = time.time()

    def end(self, type_name, result_id=0, stat_cnt=1):
        end_time = time.time()
        global g_stat
        g_stat.add_stat(type_name, result_id, self.begin_time, end_time, stat_cnt)

class StatManager(object):
    """
        统计管理
    """
    def __init__(self):
        self.logger = print
    
    def write_to_log(self, write_to_log_interval=60, process_end=False):
        global g_stat
        out_str = g_stat.get_stat_str(write_to_log_interval, process_end)
        if out_str is not None:
            self.logger(out_str)
            g_stat.clear()

if __name__ == "__main__":
    stat_mgr = StatManager()
    stat_node = StatNode("test")
    time.sleep(1)
    stat_node.end("test")
    stat_mgr.write_to_log(write_to_log_interval=0.1)
