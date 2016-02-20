import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode

import redis
import json
from torndb import Connection

from sample_notebook.CTR_EstimationModel import CTR_Estimation

r = nil

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        cpc = int(r.get('cpc'))

        data = tornado.escape.json_decode(self.request.body)
        # document = CTR_Estimation()
        # ctr = document.estimation(data)
        ctr = 0.1
        advertiserId = 1
        price = cpc * ctr

        self.responseJson(data['id'], price, advertiserId)

    def responseJson(self, data, price, advertiserId):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        json = {
            'id': id,
            'bidPrice': cpc * ctr, #[advertiserId],
            'advertiserId': advertiserId
        }
        self.write(json_encode(json))

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
    r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
