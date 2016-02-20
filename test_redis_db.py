'''
Created on 2016/02/21

@author: develop
'''

from sqlalchemy import create_engine, exc
import redis

if __name__ == '__main__':
    #SQLの実行方法
    DATABASE = 'mysql://team_f:password@dataallin.ca6eqefmtfhj.ap-northeast-1.rds.amazonaws.com:3306/db'
    engine = create_engine(DATABASE, pool_size=20, max_overflow=0)
    c = engine.connect()
    try:
        select=c.execute("SELECT * FROM requests WHERE request_id = 'ididid'")
        for s in select:
            print(s)
            print(s[0])
        c.close()
    except exc.DBAPIError, e:
        print(e)
    
    #redisの入出力方法    
    #r = redis.StrictRedis(host='elc-002.wlnxen.0001.apne1.cache.amazonaws.com', port=6379, db=0)
    #print(r.get('hoge'))
    #r.set('hoge', 'hello')
    #print(r.get('hoge'))
        
    