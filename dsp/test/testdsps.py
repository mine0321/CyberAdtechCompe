# -*- coding: utf-8 -*-
'''
Created on 2016/02/20

@author: develop
'''
import unittest
from dsp.dsp1 import Dsp1
from dsp.dsp2 import Dsp2

from dsp.util.load_sample_log import LoadSampleLog
from random import *

class TestDSPs(unittest.TestCase):

    def testName(self):
        #learn = LoadSampleLog.LoadData(start=0,end=903032)#start~endのデータを読み出し
        #test = LoadSampleLog.LoadData(start=903033)
        # learnDict = LoadSampleLog.CreateDictionary(learn)
        
        Dsps = []
        Dsps.append(Dsp1)
        Dsps.append(Dsp2)
        
        id = 0
        #for data in test: #intern_samplelog.csvを　テスト用と学習用に分けるのもありかもしれない
        for data in LoadSampleLog.LoadDataGenerator(path="../../data/intern_samplelog.csv"):
            id+=1
            
            #入札させる
            prices=[]
            advertisers=[]
            for dsp in Dsps:
                price,advertiser = dsp.bit(id, data[0], data[1], data[2], data[3])
                prices.append(price)
                advertisers.append(advertiser)
            
            
            max_price = max(prices)
            
            #second_priceを決定
            sorted_prices = sorted(prices, reverse=True)
            if len(prices)==0:continue#no win_notice
            elif len(prices)==1:second_price=max_price
            else :second_price=sorted_prices[1]+1
            
            #winnerを決定
            max_price_dsps = []#最高金額を入札したDSPの番号
            i=0
            for p in prices:
                if p==max_price : max_price_dsps.append(i)
                i+=1
            
            winner = max_price_dsps[randint(0,len(max_price_dsps)-1)]#最高額を入札したDSPからランダムにDSPを選ぶ0 <= N <= len(p)-1
            #winner = prices.index(max_price)
            
            #適当なクリック率を算出しサンプリング
            selected_advertiser=advertisers[winner]#for calc click rate
            #とりあえず適当なクリック率 click rate
            r = random()#[0.0, 1.0)
            if r<0.3: isClick=1
            else :isClick=0
            
            #win notice
            Dsps[winner].notice(id,second_price,isClick)
            
            print(winner,second_price)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
