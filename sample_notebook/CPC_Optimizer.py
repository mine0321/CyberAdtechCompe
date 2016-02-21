
# coding: utf-8

import numpy as np
import time as ti
from IPython.core.tests.test_formatters import numpy
import json
import copy

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
            8000000, 4000000, 4000000, 2000000, 2000000])  # この値は更新しない
        self.target_cpcs = [200, 133, 100, 80, 67, 57, 50, 44, 40, 36]  # この値は更新しない
        self.limit_time = float(60 * 60 * 3)  # この値は更新しない

    def optimizer(
            self, ad_num, cpcs, pre_cpcs, cost_list, pre_cost_list,
            pre_time_list, starttime):
        # 更新する広告主番号、cpc,前回のcpc,現在までに使った金額、前回までに使った金額、前回の時間()
        
        cpc = cpcs[ad_num]
        pre_cpc = pre_cpcs[ad_num]
        cost = cost_list[ad_num]
        pre_cost = pre_cost_list[ad_num]
        time = ti.time()
        pre_time = pre_time_list[ad_num]
        budget = self.budget_list[ad_num]
        
        target_cpc = self.target_cpcs[ad_num]
        
        time_rate = (time - starttime) / self.limit_time
        # 時間の消費比,最初から今回までの時間/全時間
        pre_time_rate = (pre_time - starttime) / self.limit_time
        #  時間の消費比,最初から前回までの時間/全時間
        budget_rate = cost / float(budget)
        # 予算の消費比,最初から今回までに使った予算/全予算
        pre_budget_rate = pre_cost / float(budget)
        # 予算の消費比,最初から前回までに使った予算/全予算
        beta = budget_rate / time_rate
        # １より多いと予算を使いすぎ,1より少ないと予算を使わなすぎ
        pre_beta = pre_budget_rate / pre_time_rate
        # 負の相関を調べる
        # cpc_diff = cpc - pre_cpc
        # beta_diff = beta - pre_beta
        # error_flag = cpc_diff * beta_diff
        # 負の相関の時はCPC=0,予算使用率βが0だったとする
        # if error_flag < 0:
        #     pre_cpc = 0
        #    pre_beta = 0

        # ニュートン法
        cpc_diff = cpc - pre_cpc
        beta_diff = beta - pre_beta
        beta_diff_to_target = 1 - pre_beta

        # 全然入札できていない時は広告主の予算の10%分上げる
        if beta == 1:
            return cpcs, pre_cpcs, pre_cost_list, pre_time_list
        if beta_diff == 0:
            return cpcs, pre_cpcs, pre_cost_list, pre_time_list
            # next_cpc = target_cpc  # * 0.1 + pre_cpc
        else:
            next_cpc = cpc_diff * beta_diff_to_target / float(beta_diff) + pre_cpc  # ニュートン法
            if next_cpc == cpc:
                return cpcs, pre_cpcs, pre_cost_list, pre_time_list

        if next_cpc < 0:
            next_cpc = 0
        elif target_cpc < next_cpc:
            next_cpc = target_cpc

        pre_cpcs = copy.copy(cpcs)
        cpcs[ad_num] = next_cpc

        pre_cost_list[ad_num] = cost
        pre_time_list[ad_num] = time

        #新しいcpcsと、次の計算のために指定した広告主について更新したpre_cpcs, pre_cost_list, pre_time_listを返す
        return cpcs, pre_cpcs, pre_cost_list, pre_time_list

if __name__ == '__main__':
    document = Optimizer()

    #サンプルデータ
    ad_num = 1
    list_length = 10
    cpcs = [200, 133 ,100 ,80 ,67 ,57 ,50 ,44 ,40 ,36 ]#target_cpcを初期値とする
    pre_cpcs = [0,0,0,0,0,0,0,0,0,0]#0を初期値とする
    cost_list    = [20000, 13030 ,10000 ,8000 ,6700 ,5700 ,5000 ,4400 ,4000 ,3600 ]#広告主毎の最初から現在までにかかった費用
    pre_cost_list= [0,0,0,0,0,0,0,0,0,0]#0を初期値とする
    time=ti.time()
    ti.sleep(1)
    pre_t=ti.time()
    ti.sleep(1)
    pre_time_list= [pre_t,pre_t,pre_t,pre_t,pre_t,pre_t,pre_t,pre_t,pre_t,pre_t]
    
    
    #ここより上の処理はサンプルデータを作るための処理。実際に必要な処理はここより下の処理
    #以下のad_num,cost_list,json_data_input
    ad_num=ad_num#Handlerの入力値
    cost_list=cost_list#DBから集計
    dict_data_input={"cpcs":cpcs,
                     "pre_cpcs":pre_cpcs,
                     "cost_list":cost_list,
                     "pre_cost_list":pre_cost_list,
                     "pre_time_list":pre_time_list,
                     "starttime":time
                    }
    json_data_input=json.dumps(dict_data_input, indent=4)#KVSから取ってくる値
    
    dict_data_input=json.loads(json_data_input)#デコードする
    cpcs=         dict_data_input["cpcs"]
    pre_cpcs=     dict_data_input["pre_cpcs"]
    cost_list=    dict_data_input["cost_list"]
    pre_cost_list=dict_data_input["pre_cost_list"]
    pre_time_list=dict_data_input["pre_time_list"]
    time=         dict_data_input["starttime"]
    
    
    cpcs, pre_cpcs, pre_cost_list, pre_time_list = document.optimizer(
        ad_num, cpcs, pre_cpcs, cost_list, pre_cost_list, pre_time_list,time)
    
    
    dict_data_output={"cpcs":cpcs,
                     "pre_cpcs":pre_cpcs,
                     "cost_list":cost_list,
                     "pre_cost_list":pre_cost_list,
                     "pre_time_list":pre_time_list,
                     "starttime":time
                    }
    
    #これをKVSに保存する
    json_data_output=json.dumps(dict_data_input, indent=4)
    
    print(json_data_output)
    print(cpcs)
    print(pre_cpcs)
    print(pre_cost_list)
    print(pre_time_list)
