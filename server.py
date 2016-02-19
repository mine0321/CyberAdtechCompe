import tornado.ioloop
import tornado.web
import tornado.httpserver
import redis
from tornado.web import gen

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
        foo = r.get('foo')
        self.write(foo)

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

application = tornado.web.Application([
    (r"/", MainHandler),(r"/health", HealthHandler)
],
)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
