# -*- coding: utf-8 -*-
'''
Created on 2016/02/19

@author: develop
'''
from operator import add,sub,mul,truediv
from CodeWarrior.CodeWarrior_suite import target
#メソッドの中で定義すればインスタンス変数でFOO
#クラス内で定義すればクラス変数Dsp1.FOO
class Dsp1():
    num_all_request=2000 * 60 * 60 * 3#2000QPS * 60s * 60s * 3h
    
    
    isRemainBudgets = (True,True,True,True,True,True,True,True,True,True)#予算が残っているか
    all_budgets = [20000000,12000000,12000000,8000000,8000000,8000000,4000000,4000000,2000000,2000000]#総予算
    budgets = [20000000,12000000,12000000,8000000,8000000,8000000,4000000,4000000,2000000,2000000]#残っている金額(初期値は予算)
    target_cpc = (200, 133 ,100 ,80 ,67 ,57 ,50 ,44 ,40 ,36 )#CPC（クリック単価）の最大値
    #この辺の変数はElastic casheにあとで移す
    current_cpc= [130, 100 ,80  ,60 ,50 ,40 ,30 ,35 ,30 ,30 ]#現在試しているCPC(CPCの初期値)
    old_cpc=     [  0,   0 ,  0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]#過去に試したCPCを入れておく（初期値は0にしておく）
    #current_beta=[None,None,None,None,None,None,None,None,None,None]#まだ計算していない
    old_beta=    [  0,   0 ,  0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]#CPCが0ならβは試すまでもなく0
    
    log={}#過去にどう入札したかの情報[id:advertiser]
    
    def __init__(self):
        print "create testclass"
    
    @classmethod
    def bit(id=None,site=None,floor_price=None,user=None,os=None):
        #入札処理
        ctr=Dsp1.ctr(site,floor_price,user,os)#各広告のctr(クリック率)を予測
        cpc=Dsp1.cpc(site,floor_price,user,os,ctr)#各広告のcpc(クリック単価)を計算
        price,advertiser=Dsp1.price(ctr,cpc)#price(入札金額)とadvertiser(広告主)を決定
        
        #どの広告主で入札したか記録しておく
        Dsp1.log[id]=advertiser
        
        return price*1000,advertiser #ここで1000倍する 

    @staticmethod
    def ctr(site=None,floor_price=None,user=None,os=None):
        return [0.2, 0.133 ,0.100 ,0.80 ,0.67 ,0.57 ,0.50 ,0.44 ,0.40 ,0.36 ]

    @staticmethod
    def cpc(site=None,floor_price=None,user=None,os=None,ctr=None):
        return Dsp1.current_cpc
    
    @staticmethod
    def price(ctr=None,cpc=None):#使う広告とクリック単価を決める
        prices = map(mul,ctr,cpc)
        prices = [x if x<y else y for (x, y) in zip(prices, Dsp1.budgets)]#残りの予算までしか入札できない
        price = max(prices)#クリック単価の最大値を取得
        advertiser = prices.index(price)#最大となる広告主番号を取得
        return price, advertiser
    
    @classmethod
    def notice(id,price,isClick):
        selected_advertiser=Dsp1.log[id]
        Dsp1.budgets[selected_advertiser]=Dsp1.budgets[selected_advertiser]-price
        return Dsp1.budgets[selected_advertiser]
    
    
    @classmethod
    def executebeta(cls,request_span,used_budget_span):
        timeRate=float(request_span)/Dsp1.num_all_request#時間の消費比,前回のバッチ処理から今回までにあったリクエスト数/全リクエスト数
        timeRate=[timeRate for b in Dsp1.all_budgets]#timeRateを行列にする
        budgetRate=map(truediv,used_budget_span,Dsp1.all_budgets)# 予算の消費比,前回のバッチ処理から今回までに使った予算/全予算
        
        #target_cpc*beta = cpcとなる広告主毎の値
        beta = map(truediv,budgetRate,timeRate)#１より多いと予算を使いすぎ,1より少ないと予算を使わなすぎ
        
        return beta
    
    @classmethod
    def update_cpc(cls,current_beta):#ニュートン法で次のCPCを決める。入力は現在のβ
        #CPCnext=(CPCc-CPCo)*(1-betao)/(betac-betao)+CPCo
        #(CPCc-CPCo)/(betac-betao)<0で負の相関なら、（CPCoを0、beta0を0だったことにして前回の値は使わない）
        
        next_cpc=[]
        for i in range(0, 10):#0~9
            current_c = Dsp1.current_cpc[i]
            old_c     = Dsp1.old_cpc[i]
            current_b = current_beta[i]
            old_b     = Dsp1.old_beta[i]
            
            #負の相関を調べる
            cpc_diff = current_c - old_c
            beta_diff= current_b - old_b
            error_flag=cpc_diff*beta_diff           
            #負の相関の時は　CPC=0,予算使用率βが0だったとする
            if error_flag<0:
                old_c=0
                old_b=0
            
            #ニュートン法
            cpc_diff = current_c - old_c
            beta_diff= current_b - old_b
            beta_diff_to_target=1- old_b
            
            #全然入札できていない時は広告主の予算の10%分上げる
            if beta_diff==0 :
                next_cpc+=Dsp1.target_cpc*0.1
            else:next_c=cpc_diff*beta_diff_to_target/float(beta_diff) + old_c#ニュートン法
            
            next_cpc.append(next_c)
        Dsp1.current_cpc=next_cpc
        
        return next_cpc
