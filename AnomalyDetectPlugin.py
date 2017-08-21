import numpy as np
from sklearn.svm import SVC
from Base import PluginBase
import setting
from Utils.PCA import trainPCA,testSPE
from sklearn.externals import joblib
class AnomalyDetectPlugin(PluginBase):
    pipe_Out = {'SPE':np.ndarray,'res':np.ndarray}
    pipe_In = {'res':np.ndarray,'vec':list}
    def __init__(self,N=1000,c=2.65,q=0.95,tagMeans=setting.TAG_MEAN):
        self._N=N
        self._c=c
        self._q=q
        self._tagMeans=tagMeans
    def fit(self,In,y=None,**args):
        print ("start anomaly detecting")
        trainPCA(self._N, self._c, self._q, [[tag, self._tagMeans[tag]] for tag in self._tagMeans], False)
        print ("finish anomaly detecting")
        return self
    def transform(self,In,y=None,**params):
        out=self.predict(In)
        return out

    def predict(self,In):
        _res=self.fetch(In,vec=list,res=np.ndarray)
        X = _res['vec']
        y = _res['res']
        SPE = np.zeros(len(y))
        test_Vec=np.array(X)
        for type in self._tagMeans:
            _X_ = test_Vec[y == type]
            if (len(_X_) == 0):
                continue
            SPE[y == type] = testSPE(_X_, type)
        out=In
        out['SPE']=SPE
        out['res']=y
        return out

    def score(self,X,y=None,**params):
        out=self.predict(X)
        res=out['res']
        SPE=out['SPE']
        predict_accuracy=sum(res==y)*1.0/len(res)
        anomaly_detect_accuracy=sum(np.logical_not(np.logical_or(SPE,res==y)))*1.0/sum(SPE==False)
        anomaly_detect_recall=sum(np.logical_not(np.logical_or(SPE,res==y)))*1.0/sum((res==y)==False)
        print sum(SPE==0),sum((res==y)==False)
        out['predict_accuracy']=predict_accuracy
        out['anomaly_detect_accuracy']=anomaly_detect_accuracy
        out['anomaly_detect_recall']=anomaly_detect_recall
        return out