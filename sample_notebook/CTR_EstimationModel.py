
# coding: utf-8

import xgboost as xgb
from sklearn.externals import joblib

class CTR_Estimation(object):
    """docstring for CTR_Estimation"""
    # input : dict format
    # output : list format  ( Advertiser order)
    #
    # e.g.)
    # document = CTR_Estimation(sample_dict)
    # document.estimation(sample_dict)
    #
    def __init__(self):
        self.xgb_models = [joblib.load(
            '../models/Ad%d_xgb.pkl' % ind) for ind in xrange(1, 11)]
        self.modnum = 3

    def estimation(self, sample_dict):
        if sample_dict['floorPrice'] == 'nan':
            sample_dict['floorPrice'] = 0
        if sample_dict['device'] == 'iOS':
            test_sample = xgb.DMatrix(
                [self.hashnum(self.modnum, sample_dict['site']),
                    self.hashnum(self.modnum, sample_dict['user']), 0,
                    sample_dict['floorPrice']])
        else:
            test_sample = xgb.DMatrix([
                self.hashnum(self.modnum, sample_dict['site']),
                self.hashnum(self.modnum, sample_dict['user']), 1,
                sample_dict['floorPrice']])
        return [float(model.predict(test_sample))for model in xgb_models]

    def hashnum(self, modnum, data):
        mod = 10 ** modnum
        return hash(data) % mod
