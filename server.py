import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode
import numpy as np

import redis
import json

from sqlalchemy import create_engine, exc
from sample_notebook.CPC_Optimizer import Optimizer
from sample_notebook.CTR_EstimationModel import CTR_Estimation

DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)

        #KVSからjsonを取得
        json_data_input=r.get('json')
        dict_data_input=json.loads(json_data_input)#デコードする
        cpc=dict_data_input["cpcs"]
        
        data = tornado.escape.json_decode(self.request.body)
        ctr = document.estimation(data)
        bit_list = np.array(ctr) * np.array(cpc)
        advertiserId = str(np.argmax(bit_list))
        bit = np.max(bit_list)

        self.responseJson(data['id'], bit, 0.1, advertiserId)
        self.insertData(
            data['id'], data['floorPrice'], data['site'], data['device'],
            data['user'], advertiserId, bit, 0, 0, data['id'])

    def responseJson(self, id, cpc, ctr, advertiserId):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        json = {
            'id': id,
            'bidPrice': cpc * ctr, #[advertiserId],
            'advertiserId': advertiserId,
        }
        self.write(json_encode(json))

    def insertData(self, id, floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id):
        c = engine.connect()
        try:
            c.execute("""INSERT INTO requests (floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}, '{8}')""".format(floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id))
            c.close()
        except exc.DBAPIError, e:
            print(e)
            # if e.connection_invalidated:
            #     pass


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        print("Hello")

class WinHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.updateData(data['id'], data['price'], data['isClick'])

    def updateData(self, request_id, second_price, is_click):
        c = engine.connect()
        try:
            c.execute("""UPDATE requests SET second_price = {0}, is_click = {1} WHERE request_id = '{2}'""".format(second_price, is_click, request_id))
            c.close()
        except exc.DBAPIError, e:
            print(e)
            # if e.connection_invalidated:

class CpcHandler(tornado.web.RequestHandler):
    
    def initJson(self,r=None,c=None):
        if r==None:
            r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        if c==None:
            c = engine.connect()
        r.set("initFlag","hoge")
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
                         "pre_time_list":pre_time_list
                        }
        json_data_output=json.dumps(dict_data_output, indent=4)#KVSから取ってくる値
        r.set('json', json_data_output)
        
    
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        c = engine.connect()
        #キーがいないなら初期値を設定(starttimeがいるのでこれは重要)
        if not r.exists("initFlag"):
            self.init_json(r,c)
        
        ad_num = int(data["ad_num"])
        
        #DBから使った費用を取得
        cost_list=[0 for i in range(0,10)]
        try:
            select=c.execute("SELECT advertiser_id,sum(second_price) as cost FROM db.requests GROUP BY advertiser_id;")
            for s in select:
                cost_list[int(s[0])]=int(s[1])
        except exc.DBAPIError, e:
            print(e)

        #DBからstart_timeを取得
        start_time=None
        try : 
            select=c.execute("SELECT id, UNIX_TIMESTAMP(created_at) as starttime FROM db.requests ORDER BY id LIMIT 1;")
            for s in select:
                start_time=int(s[1])
        except exc.DBAPIError, e:
            print(e)
        
        #KVSからjsonを取得
        json_data_input=r.get('json')
        dict_data_input=json.loads(json_data_input)#デコードする
        cpcs=         dict_data_input["cpcs"]
        pre_cpcs=     dict_data_input["pre_cpcs"]
        pre_cost_list=dict_data_input["pre_cost_list"]
        pre_time_list=dict_data_input["pre_time_list"]
        
        #Optimizer実行して
        document = Optimizer()
        cpcs, pre_cpcs, pre_cost_list, pre_time_list = document.optimizer(
            ad_num, cpcs, pre_cpcs, cost_list, pre_cost_list, pre_time_list,start_time)
        
        #KVSに値を保存する
        dict_data_output={"cpcs":cpcs,
                     "pre_cpcs":pre_cpcs,
                     "pre_cost_list":pre_cost_list,
                     "pre_time_list":pre_time_list
                        }
        json_data_output=json.dumps(dict_data_input, indent=4)
        r.set('json', json_data_output)
        try : 
            select=c.execute("SELECT id, UNIX_TIMESTAMP(created_at) as starttime FROM db.requests ORDER BY id LIMIT 1;")
            for s in select:
                start_time=int(s[1])
                c.close()
        except exc.DBAPIError, e:
            print(e)
        


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/win", WinHandler),
    (r"/cpc", CpcHandler)
],
)

if __name__ == "__main__":
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    document = CTR_Estimation()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
