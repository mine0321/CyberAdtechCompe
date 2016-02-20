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


    def testBit(self):
        self.assertEqual(1, 1, "ErrorMessage")

        print(Dsp1.bit(1, 2, 3, 4))
        first = Dsp1.notice(1,2)
        
        print(Dsp1.bit(2, 2, 3, 4))
        second = Dsp1.notice(2,2)
        self.assertNotEqual(first, second, "budgetが更新されてません")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()