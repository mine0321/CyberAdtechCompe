
# coding: utf-8

import numpy as np
import time


class Optimizer(object):
    """docstring for Optimizer."""
    #
    # e.g.)
    # document = Optimizer()
    # document.optimizer(ad_num, pre_cpcs, cpcs, cost_list)
    #
    def __init__(self):
        self.budget_list = np.array([
            20000000, 12000000, 12000000, 8000000, 8000000,
            8000000, 4000000, 4000000, 2000000, 2000000])
        self.starttime = time.time()
        self.limit_time = float(60 * 60 * 3)

    def optimizer(self, ad_num, cpcs, pre_cpcs, cost_list):
        """ 最適化アルゴリズムを記述"""
        return cpcs, pre_cpcs, cost_list

if __name__ == '__main__':
    document = Optimizer()
    ad_num = 1
    list_length = 10
    cpcs = np.array([130, 100, 80, 60, 50, 40, 30, 35, 30, 30])
    pre_cpcs = np.zeros(list_length)
    cost_list = np.zeros(list_length)
    cpcs, pre_cpcs, cost_list = document.optimizer(
        ad_num, cpcs, pre_cpcs, cost_list)
