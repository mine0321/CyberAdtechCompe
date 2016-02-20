
# coding: utf-8

import xgboost as xgb
from sklearn.externals import joblib


def hashnum(modnum, data):
    mod = 10 ** modnum
    return hash(data) % mod

xgb_models = [
    joblib.load('../models/Ad%d_xgb.pkl' % ind) for ind in xrange(1, 11)]

sample_dict = {
    'id': "ididid",
    'floorPrice': 1000,
    'site': "medianame",
    'device': "device",
    'user': "a9102910201",
    'test': 0
}

if __name__ == '__main__':

    modnum = 3

    if sample_dict['floorPrice'] == 'nan':
        sample_dict['floorPrice'] = 0
    if sample_dict['device'] == 'iOS':
            test_sample = xgb.DMatrix(
                [hashnum(modnum, sample_dict['site']),
                    hashnum(modnum, sample_dict['user']), 0,
                    sample_dict['floorPrice']])
    else:
        test_sample = xgb.DMatrix([
            hashnum(modnum, sample_dict['site']),
            hashnum(modnum, sample_dict['user']), 1,
            sample_dict['floorPrice']])
    [float(model.predict(test_sample))for model in xgb_models]
