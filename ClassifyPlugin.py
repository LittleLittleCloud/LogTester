import numpy as np
from sklearn.svm import SVC
from Base import PluginBase
import setting
from sklearn.externals import joblib
class ClassifyPlugin(PluginBase,SVC):
    pipe_In = {'vec':list}
    pipe_Out = {'res':np.ndarray,'vec':list}
    def fit(self, In, y, sample_weight=None,**params):
        res=self.fetch(In,vec=list)
        X=res['vec']
        print ("start training")
        super(ClassifyPlugin,self).fit(X,y,sample_weight)
        print("finish training")
        if params['cache']==True:
            joblib.dump(self, setting.ROOT_PATH + '\Models\\SVM')
        return self
    def transform(self,In,y=None):
        res=self.fetch(In,vec=list)
        X=res['vec']
        _res=super(ClassifyPlugin,self).predict(X)
        out=In
        out['res']=_res
        out['vec']=X
        return out