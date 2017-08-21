import numpy as np
from sklearn import datasets
import json
from sklearn.decomposition import PCA
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import math
import setting


# N: the dimension to keep
# c: the 1-a percentile of normal distribute
# _r: the percentage that remain for normal components
def trainPCA(N, c, _r, taglist, draw):
    with open(setting.FEATURE_PATH, 'r') as f:
        vec = json.load(f)
    _X = np.array([i[0] for i in vec])
    y = np.array([i[1] for i in vec])
    # store the Q value
    res = []
    for [tagindex, tagName] in taglist:
        X = _X[y == tagindex]
        if len(X) == 0:
            res.append([0, 0])
            continue
        X_z = X - np.mean(X, axis=0)
        U,T,V=np.linalg.svd(X_z)
        components=V
        if not draw:
            np.save(setting.MODEL_PATH+str(tagindex),V)
            np.save(setting.MODEL_PATH+str(tagindex)+'mean',np.mean(X, axis=0))
        vars=T*T/(len(X)-1)
        r = 0
        varsum=sum(vars)
        for i in range(len(vars)):
            if sum(vars[:i])/varsum > _r:
                r = i
                break

        try:
            o1 = np.sum(np.power(vars, 1)[r:])
            o2 = np.sum(np.power(vars, 2)[r:])
            o3 = np.sum(np.power(vars, 3)[r:])
            if o2*o1*o3==0.0:
                raise ValueError
            h0 = 1 - 2.0 * o1 * o3 / (3 * o2 * o2)
            t1 = (c * math.sqrt(2 * o2 * h0 * h0) / o1) + 1 + (o2 * h0 * (h0 - 1) / (o1 * o1))
            t2 = 1.0 / h0

            theta = o1 * math.pow(t1, t2)

        except ValueError as w:
            theta = 0.1

        qlist = []

        for x in X_z:
            B = np.dot(components[:r].transpose(), components[:r])
            A = np.eye(len(x)) - B
            q = np.dot(np.dot(x.transpose(), A), x)
            qlist.append(q)
        res.append([theta,r])
        if draw:
            print theta
            plt.scatter(np.arange(len(X)), qlist, alpha=.8, lw=2,label=[])
            plt.show()
    if not draw:
        with open(setting.RESULT_PATH + 'Q_val.json', 'w') as f:
            json.dump(res, f)
    return res
    # plt.show()


def SetQ_val(type, val):
    with open(setting.RESULT_PATH + 'Q_val.json', 'r') as f:
        Q_val = json.load(f)
    Q_val[type][0] = val
    print "successfully set val: " + str(val) + " at " + str(type)
    with open(setting.RESULT_PATH + 'Q_val.json', 'w') as f:
        json.dump(Q_val, f)


def DrawQ_distrubute(N, c, r, type):
    trainPCA(N, c, r, [[type, '']],True)


def testSPE(featureVec, type):
    V=np.load(setting.MODEL_PATH+str(type)+'.npy')
    mean=np.load(setting.MODEL_PATH+str(type)+'mean.npy')
    with open(setting.RESULT_PATH + 'Q_val.json', 'r') as f:
        Q_val = json.load(f)
    theta = Q_val[type][0]
    r=Q_val[type][1]
    components = V
    B = np.dot(components[:r].transpose(), components[:r])
    A = np.eye(len(B)) - B
    featureVec=featureVec-mean
    q = np.dot(np.dot(featureVec, A), featureVec.transpose())
    return q<theta


if __name__ == '__main__':
    DrawQ_distrubute(1000,2.6,0.9,13)
    SetQ_val(13,10)