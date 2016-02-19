import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
import time


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.write("hello world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
