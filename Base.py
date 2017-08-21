import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin,clone
class PluginBase(TransformerMixin,BaseEstimator):
    #should return an instanse of this class


    @classmethod
    def fetch(cls,In,**args):
        res={}
        for key in args:
            if key in In and args[key]==type(In[key]):
                res[key]=In[key]
            else:
                raise BaseException(cls.__name__+' data {0} not match, type: {1}, expect: {2}'.format(key,type(args[key]),type(In[key])))
        return res

    @classmethod
    def check_pipeIn(cls,In):
        for t in In:
            if type(In[t]) not in cls.pipe_In.values():
                raise BaseException('input data not match, input data {0} doesn\'t match'.format(t))

    @classmethod
    def check_pipeOut(cls,Out):
        for t in Out:
            if type(Out[t]) not in cls.pipe_Out.values():
                raise BaseException(cls.__name__+' output data {0} not match, type: {1}, expect: {2}'.format(t,type(Out[t]),cls.pipe_Out.values()))
    pipe_In=None
    pipe_Out=None
    def __str__(self):
        return "{0}, pipe_In:{1}, pipe_Out:{2}".format(self.__class__,self.pipe_In,self.pipe_Out)

class InputPluginBase(PluginBase):
    def fit(self,In,y=None,**args):
        pass
    def transform(self,X,**args):
        pass
class FeaturePluginBase(PluginBase):
    def fit(self,In,y=None,**args):
        pass

    def transform(self,X,**args):
        pass
class ClassifyPluginBase(PluginBase):
    def fit(self,In,y=None,**args):
        pass

    def transform(self,X,**args):
        pass
class OutputPluginBase(PluginBase):
    def fit(self,In,y=None,**args):
        pass

    def transform(self,X,**args):
        pass
