# -*- coding: utf-8 -*-
'''
Created on 2016/02/19

@author: develop
'''
from operator import mul
from dsp.util.load_sample_log import LoadSampleLog
#メソッドの中で定義すればインスタンス変数でFOO
#クラス内で定義すればクラス変数Dsp2.FOO
class Dsp2():
    isRemainBudgets = (True,True,True,True,True,True,True,True,True,True)#予算が残っているか
    budgets = [20000000,12000000,12000000,8000000,8000000,8000000,8000000,4000000,4000000,2000000,2000000]#残っている金額(初期値は予算)
    target_cpc = (200, 133 ,100 ,80 ,67 ,57 ,50 ,44 ,40 ,36 )#CPC（クリック単価）の最大値
    
    log={}#過去にどう入札したかの情報[id:advertiser]
    
    dict={}
    
    def __init__(self):   
        print "create testclass"
    
    @classmethod
    def setDict(cla,d={}):
        cla.dict=d
    
    @classmethod
    def bit(cla,id=None,site=None,floor_price=None,user=None,os=None):
        
        
        #入札処理
        ctr=Dsp2.ctr(site,floor_price,user,os)#各広告のctr(クリック率)を予測
        cpc=Dsp2.cpc(site,floor_price,user,os,ctr)#各広告のcpc(クリック単価)を計算
        price,advertiser=Dsp2.price(ctr,cpc)#price(入札金額)とadvertiser(広告主)を決定
        
        #どの広告主で入札したか記録しておく
        Dsp2.log[id]=advertiser
        
        return int(price*1000),advertiser #ここで1000倍する 

    @staticmethod
    def ctr(site=None,floor_price=None,user=None,os=None):
        return [0.2, 0.133 ,0.100 ,0.80 ,0.67 ,0.57 ,0.50 ,0.44 ,0.40 ,0.36 ]

    @staticmethod
    def cpc(site=None,floor_price=None,user=None,os=None,ctr=None):
        return [201, 134 ,101 ,81 ,68 ,58 ,51 ,45 ,41 ,37 ]
    
    @staticmethod
    def price(ctr=None,cpc=None):#使う広告とクリック単価を決める
        prices = map(mul,ctr,cpc)
        prices = [x if x<y else y for (x, y) in zip(prices, Dsp2.budgets)]#残りの予算までしか入札できない
        price = max(prices)#クリック単価の最大値を取得
        advertiser = prices.index(price)#最大となる広告主番号を取得
        return price, advertiser
    
    @classmethod
    def notice(cla,id,price,isClick):
        selected_advertiser=Dsp2.log[id]
        Dsp2.budgets[selected_advertiser]=Dsp2.budgets[selected_advertiser]-price/1000#とりあえずsecond_priceを1000で割った値を引く。予算を千倍しておくのも手かも。
        return Dsp2.budgets[selected_advertiser]