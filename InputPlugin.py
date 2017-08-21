import numpy as np
from Base import InputPluginBase
import setting
class InputPlugin(InputPluginBase):
    pipe_In = {'id':list,'type':list}
    pipe_Out = {'id_feature':list}
    def __init__(self,Sessions=None):
        self.sessions=Sessions
    def fit(self,X,y=None,**params):
        return self
    def transform(self,In,**params):
        #[id,feature]
        out=In
        res=self.fetch(In,Sessions=dict,id=np.ndarray)
        Data=res['id']
        self.sessions=res['Sessions']
        res=get_Sessions_From_Data(self.sessions,Data)
        out['id_feature']=res
        out['Sessions']=self.sessions
        return out


def get_Sessions_From_Data(Session,Data):
    res=[]
    for id in Data:
        if id in Session:
            res.append([id,''.join(Session[id]['feature'])])
    return res
