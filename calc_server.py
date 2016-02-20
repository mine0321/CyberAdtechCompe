import tornado.ioloop
import tornado.web
import tornado.httpserver
import redis
import json
from tornado.web import gen

from sqlalchemy import create_engine, exc

REDIS_HOST = 'elc-002.wlnxen.0001.apne1.cache.amazonaws.com'
DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        print("Hello")

class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        data = tornado.escape.json_decode(self.request.body)
        self.write(data)

application = tornado.web.Application([
    (r"/health", HealthHandler),
    (r"/update", UpdateHandler)
],
)

if __name__ == "__main__":
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
