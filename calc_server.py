import tornado.ioloop
import tornado.web
import tornado.httpserver
import redis
import json
import torndb
from tornado.web import gen

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db = torndb.Connection("dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306", "db", user='team_f', password='password')
	rows = db.query("select Id,Title from post")
	self.write("ssss")

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
