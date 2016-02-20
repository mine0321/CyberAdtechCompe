import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode

import redis
import json

from sqlalchemy.pool import QueuePool
import sqlalchemy.pool as pool
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base

from sample_notebook.CTR_EstimationModel import CTR_Estimation

Base = declarative_base()
DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        cpc = int(r.get('cpctest'))
        data = tornado.escape.json_decode(self.request.body)
        ctr = document.estimation(data)
        advertiserId = '1'

        self.responseJson(data['id'], cpc, 0.1, advertiserId)
        self.insertData(data['id'], data['floorPrice'], data['site'], data['device'], data['user'], 1, 20, 0, 0)

    def responseJson(self, id, cpc, ctr, advertiserId):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        json = {
            'id': id,
            'bidPrice': cpc * ctr, #[advertiserId],
            'advertiserId': advertiserId,
        }
        self.write(json_encode(json))

    def insertData(self, id, floor_price, site, device, user, advertiser_id, bit_price, win, is_click):
        c = engine.connect()
        try:
            c.execute("""INSERT INTO requests (floor_price, site, device, user, advertiser_id, bit_price, win, is_click) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7})""".format(floor_price, site, device, user, advertiser_id, bit_price, win, is_click))
            c.close()
        except exc.DBAPIError, e:
            if e.connection_invalidated:
                pass


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class WinHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.body)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/win", WinHandler)
],
)

if __name__ == "__main__":
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    document = CTR_Estimation()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
