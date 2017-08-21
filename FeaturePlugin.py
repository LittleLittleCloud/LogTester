import numpy as np
import json
from Base import FeaturePluginBase
import setting
class FeaturePlugin(FeaturePluginBase):
    pipe_In = {'id_feature':list}
    pipe_Out = {'[vec]':list}
    def __init__(self,Sessions=None):
        self.sessions=Sessions
    def fit(self,In,y=None,**params):
        res=self.transform(In,y)
        X=res['vec']
        id_z = map(int, y)
        vec = [[x[0],x[1]] for x in zip(X, id_z)]
        with open(setting.FEATURE_PATH, 'w') as f:
            json.dump(vec, f)
        return self
    def transform(self,In,y=None,**params):
        out=In
        res=self.fetch(In,id_feature=list,Sessions=dict)
        self.sessions=res['Sessions']
        X=res['id_feature']
        patts=get_Patterns_with_3_Gram(self.sessions,In,None)
        feature=[i[1] for i in X]
        X=get_TransVec_and_TransRes(patts,feature)
        out['vec']=X
        return out

def get_Patterns_with_3_Gram(Sessions,traindata,traindataXML):
    with open(setting.PATTERN_PATH, 'r') as f:
        patts = json.load(f)
    return patts

def get_TransVec_and_TransRes(patts,X):
    # yield the feature vector
    trainVec = []
    for feature in X:
        featureVec = np.zeros(len(patts))
        for i in range(len(patts)):
            featureVec[i] += matchPatt2(patts[i], feature)
        trainVec.append(featureVec.tolist())
    return trainVec

def matchPatt2(patt,feature):
    return ''.join(feature).count(''.join(patt))