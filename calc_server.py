import tornado.ioloop
import tornado.web
import tornado.httpserver
import redis
import json
from tornado.web import gen

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.write(data)

class WinHandler(tornado.web.RequestHandler):
    def get(self):
        data = tornado.escape.json_decode(self.request.body)
        self.write(data)

application = tornado.web.Application([
    (r"/", MainHandler),(r"/win", WinHandler)
],
)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
