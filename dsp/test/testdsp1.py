# -*- coding: utf-8 -*-
'''
Created on 2016/02/19

@author: develop
'''
import unittest
from dsp.dsp1 import Dsp1

class Test(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testCpc(self):
        print(Dsp1.bit(3, 2, 4, 5, 6))
        beta=Dsp1.executebeta(2000*30,[120, 133 ,100 ,80 ,67 ,57 ,50 ,44 ,40 ,36 ])#30s分のリクエスト,120円使用
        Dsp1.update_cpc(beta)#beta
        print("hoge")

    def testBit(self):
        self.assertEqual(1, 1, "ErrorMessage")

        print(Dsp1.bit(1, 2, 3, 4, 5))
        first = Dsp1.notice(1,2000,1)
        
        print(Dsp1.bit(2, 2, 4, 5, 6))
        second = Dsp1.notice(2,2000,0)
        self.assertNotEqual(first, second, "budgetが更新されてません")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()