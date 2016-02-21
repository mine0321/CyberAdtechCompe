# coding: utf-8
'''
Created on 2016/02/21

@author: develop
'''
from server import CpcHandler
import time as ti
from sqlalchemy import create_engine, exc
import redis
import time
import json
from sample_notebook.CPC_Optimizer import Optimizer
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import gen
from tornado.escape import json_encode
import numpy as np

import redis
import json

DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'

from sqlalchemy import create_engine, exc
from sample_notebook.CPC_Optimizer import Optimizer
from sample_notebook.CTR_EstimationModel import CTR_Estimation

application = tornado.web.Application([
    (r"/cpc", CpcHandler)
],
)

if __name__ == '__main__':
    #SQLの実行方法
    cpc=CpcHandler(tornado.web.RequestHandler)
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    document = CTR_Estimation()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
    cpc.post()


    