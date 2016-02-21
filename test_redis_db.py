# coding: utf-8
'''
Created on 2016/02/21

@author: develop
'''
import time as ti
from sqlalchemy import create_engine, exc
import redis
import time
import json
from sample_notebook.CPC_Optimizer import Optimizer

if __name__ == '__main__':
    #SQLの実行方法
    DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    c = engine.connect()
    try:
        select=c.execute("SELECT * FROM requests WHERE request_id = 'ididid'")
        for s in select:
            print(s)
            print(s[0])
        select=c.execute("SELECT advertiser_id,sum(second_price) as cost FROM db.requests GROUP BY advertiser_id;")
        for s in select:
            print(s)
        #c.close()
    except exc.DBAPIError, e:
        print(e)
    
    
    #redisの入出力方法
    r = redis.Redis(host='localhost', port=6379, db=0)    
    #r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
    #print(r.get('hoge'))
    #r.set('hoge', 'hello')
    #print(r.get('hoge'))
    
    #まずcpcを集計して格納するのを書く

    #キーがいないなら初期値を設定
    if not r.exists("json"):
        cpcs = [200, 133 ,100 ,80 ,67 ,57 ,50 ,44 ,40 ,36 ]#target_cpcを初期値とする
        pre_cpcs = [0 for i in range(0,10)]#0を初期値とする
        cost_list=[0 for i in range(0,10)]#広告主毎の最初から現在までにかかった費用
        pre_cost_list= [0 for i in range(0,10)]#0を初期値とする
        start_time=None
        try : 
            select=c.execute("SELECT id, UNIX_TIMESTAMP(created_at) as starttime FROM db.requests ORDER BY id LIMIT 1;")
            for s in select:
                start_time=int(s[1])
        except exc.DBAPIError, e:
            print(e)
        pre_time_list = [start_time for i in range(0,10)]
        dict_data_output={"cpcs":cpcs,
                     "pre_cpcs":pre_cpcs,
                     "pre_cost_list":pre_cost_list,
                     "pre_time_list":pre_time_list,
                     "starttime":start_time
                    }
        json_data_output=json.dumps(dict_data_output, indent=4)#KVSから取ってくる値
        r.set('json', json_data_output)
    
    #ad_num = int(data["ad_num"])
    ad_num = 1#上に後で変える
    
    #DBから使った費用を取得
    cost_list=[0 for i in range(0,10)]
    try:
        select=c.execute("SELECT advertiser_id,sum(second_price) as cost FROM db.requests GROUP BY advertiser_id;")
        for s in select:
            cost_list[int(s[0])]=int(s[1])
        c.close()
    except exc.DBAPIError, e:
        print(e)
    
    #KVSからjsonを取得
    json_data_input=r.get('json')
    dict_data_input=json.loads(json_data_input)#デコードする
    cpcs=         dict_data_input["cpcs"]
    pre_cpcs=     dict_data_input["pre_cpcs"]
    pre_cost_list=dict_data_input["pre_cost_list"]
    pre_time_list=dict_data_input["pre_time_list"]
    starttime=    dict_data_input["starttime"]
    
    #Optimizer実行して
    document = Optimizer()
    cpcs, pre_cpcs, pre_cost_list, pre_time_list = document.optimizer(
        ad_num, cpcs, pre_cpcs, cost_list, pre_cost_list, pre_time_list,starttime)
    
    #KVSに値を保存する
    dict_data_output={"cpcs":cpcs,
                 "pre_cpcs":pre_cpcs,
                 "pre_cost_list":pre_cost_list,
                 "pre_time_list":pre_time_list,
                 "starttime":starttime
                    }
    json_data_output=json.dumps(dict_data_input, indent=4)
    r.set('json', json_data_output)
    