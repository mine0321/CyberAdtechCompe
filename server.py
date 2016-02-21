import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode
import numpy as np
import threading

import redis
# import json
#
# from sqlalchemy import create_engine, exc
# from sample_notebook.CPC_Optimizer import Optimizer
# from sample_notebook.CTR_EstimationModel import CTR_Estimation

DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        cpc = r.get('cpc')
        r.set(data['id'], self.request.body)

        # ctr = document.estimation(data)
        # cpc = np.array(cpc.items())
        cpc = np.ones(10)
        # bit_list = np.array(ctr) * np.array(cpc)


        alpha_list = tornado.escape.json_decode(r.get('alpha'))
        beta_list = tornado.escape.json_decode(r.get('beta'))

        alpha = [float(alpha_list[key]) for key in list(alpha_list)]
        beta = [float(beta_list[key]) for key in list(beta_list)]

        bit_list = 0.5 * np.array(cpc) * np.array(alpha) + np.array(beta)
        advertiserId = str(np.argmax(bit_list))
        bit = np.max(bit_list)
        # self.responseJson(data['id'], bit, advertiserId, alpha[advertiserId], beta[advertiserId])
        self.responseJson(data['id'], bit, advertiserId)

    def responseJson(self, id, bit, advertiserId):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        json = {
            'id': id,
            'bidPrice': bit,# * a + b,
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
        json = r.get(win_id)


    # def insertData(self, id, floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id):
    #     c = engine.connect()
    #     try:
    #         c.execute("""INSERT INTO requests (floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}, '{8}')""".format(floor_price, site, device, user, advertiser_id, bit_price, win, is_click, request_id))
    #         c.close()
    #     except exc.DBAPIError, e:
    #         print(e)
            # if e.connection_invalidated:
            #     pass

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/win", WinHandler),
],
)

if __name__ == "__main__":
    # engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    # document = CTR_Estimation()
    r = redis.StrictRedis(host='elc-001.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(9)
    tornado.ioloop.IOLoop.current().start()
