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
        cpc = int(r.get('cpctest'))
        data = tornado.escape.json_decode(self.request.body)
        ctr = document.estimation(data)
        cpc = np.arange(0, 10)
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
        self.write("Hello")

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

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/win", WinHandler),
],
)

if __name__ == "__main__":
    engine = create_engine(DATABASE, pool_size=100, max_overflow=0)
    document = CTR_Estimation()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(9)
    tornado.ioloop.IOLoop.current().start()
