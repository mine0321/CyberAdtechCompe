# -*- coding: utf-8 -*-
'''
Created on 2016/02/20

@author: develop
'''
import nimfa
import pandas
import numpy as np
from dsp.util.load_sample_log import LoadSampleLog
class NMF(object):
    '''
    参考：https://github.com/marinkaz/nimfa/issues/20
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @classmethod
    def getNmf(cls,path="../../data/intern_samplelog.csv"):
        #data = pandas.read_table(path,header=0)
        data = pandas.read_csv(path)
        data['site']=data['site'].str.replace("media_","")#http://stackoverflow.com/questions/24037507/converting-string-objects-to-int-float-using-pandas
        #data["floor_price"]=data["floor_price"].str.replace("NA","0")
        data["user"]=data["user"].str.replace("user_","")
        del data["click"]
        del data["advertiser"]
        del data["os"]
        del data["floor_price"]
        #data["os"]=data["os"].str.replace("iOS","1")
        #data["os"]=data["os"].str.replace("Android","2")
        vec = np.matrix(data.as_matrix())
        nmf = nimfa.Nmf(vec, seed='random_vcol', rank=20, max_iter=50)
        nmf_fit = nmf()
        
        print('Rss: %5.4f' % nmf_fit.fit.rss())
        print('Evar: %5.4f' % nmf_fit.fit.evar())
        print('K-L divergence: %5.4f' % nmf_fit.distance(metric='kl'))
        print('Sparseness, W: %5.4f, H: %5.4f' % nmf_fit.fit.sparseness())
        return nmf_fit

res=NMF.getNmf()
