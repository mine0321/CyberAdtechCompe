import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
import time
from Dsp.Dsp1 import DSP1

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

application = tornado.web.Application([
    (r"/", MainHandler),(r"/health", HealthHandler)
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
