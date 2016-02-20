# -*- coding: utf-8 -*-
'''
Created on 2016/02/20

@author: develop
'''

#learn = LoadSampleLog.LoadData(start=0,end=903032)#start~endのデータを読み出し
#test = LoadSampleLog.LoadData(start=903033)
#learnDict = LoadSampleLog.CreateDictionary(learn)

class LoadSampleLog(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @classmethod
    def LoadData(cls,start=0,end=None,path="../../data/intern_samplelog.csv"):#クラスを表す変数,引数　の順
        count = 0
        data = []
        with open(path) as f:
            for line in f:
                if end!=None and count>end:break;
                d = line.split(",")
                if '\"site\"'  == d[0] :  # 最初の一行目はスキップ
                    print(d)
                    continue
                if line.strip() == "": continue  # 改行しかない（データが入っていない場合は）スキップ
                d[5] = d[5].strip()  # 改行文字がいるので除去
                if start<=count: data.append(d)
                count += 1
        return data
    
    @classmethod
    def CreateDictionary(cls,data):#クラスを表す変数,引数　の順
        dict = {}
        for d in data:
            dict[d[0]]=d[1:4]
        return dict

    @classmethod
    def LoadDataGenerator(cls,start=0,end=None,path="../../data/intern_samplelog.csv"):#クラスを表す変数,引数　の順
        count = 0
        data = []
        with open(path) as f:
            for line in f:
                if end!=None and count>end:break;
                d = line.split(",")
                if '\"site\"'  == d[0] :  # 最初の一行目はスキップ
                    print(d)
                    continue
                if line.strip() == "": continue  # 改行しかない（データが入っていない場合は）スキップ
                d[5] = d[5].strip()  # 改行文字がいるので除去
                
                if start<=count: yield d
                count += 1
