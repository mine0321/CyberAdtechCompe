# -*- coding: utf-8 -*-
'''
Created on 2016/02/19

@author: develop
'''
import unittest
import server
import tornado
from tornado.escape import to_unicode
from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.httpclient import HTTPError

#server.pyのテスト 参考 http://www.tornadoweb.org/en/stable/testing.html
class TestServer(AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        print("testCPCHandler")
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:8080/cpc")
        # Test contents of response
        self.assertEqual("hello world", response.body)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMainHandler']
    unittest.main()