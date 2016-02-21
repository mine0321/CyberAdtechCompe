import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode
import numpy as np
import threading

import redis
import json

from sqlalchemy import create_engine, exc
from sample_notebook.CPC_Optimizer import Optimizer
from sample_notebook.CTR_EstimationModel import CTR_Estimation

DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        cpc = r.get('cpc')
        r.set(data['id'],self.request.body)

        data = tornado.escape.json_decode(self.request.body)
        # ctr = document.estimation(data)
        cpc = np.array(cpc.items())
        # bit_list = np.array(ctr) * np.array(cpc)
        bit_list = 0.5 * np.array(cpc)
        advertiserId = str(np.argmax(bit_list))
        bit = np.max(bit_list)

        alpha_list = tornado.escape.json_decode(r.get('alpha'))
        beta_list = tornado.escape.json_decode(r.get('beta'))

        self.responseJson(data['id'], bit, advertiserId, alpha_list[advertiserId], beta_list[advertiserId])

    def responseJson(self, id, bit, advertiserId, a ,b):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        json = {
            'id': id,
            'bidPrice': bit * a + b,
            'advertiserId': advertiserId,
        }
        self.write(json_encode(json))

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")


class WinHandler(tornado.web.RequestHandler):
    def post(self):
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        data = tornado.escape.json_decode(self.request.body)
        win_id = data['id']
        r.get[win_id]

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/win", WinHandler),
],
)

if __name__ == "__main__":
    # engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    # document = CTR_Estimation()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
