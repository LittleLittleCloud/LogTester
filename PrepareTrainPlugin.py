import numpy as np
import json
from Base import PluginBase
from xml.dom import minidom
class PrepareTrainPlugin(PluginBase):
    def fit(self,In,y=None,**kwargs):
        return self
    def transform(self,In,**args):
        res=self.fetch(In,Sessions_path=str,id=np.ndarray)
        Sessions_path=res['Sessions_path']
        Train_data=res['id']
        with open(Sessions_path,'r') as f:
            Sessions = json.load(f)
        out=In
        out['Sessions']=Sessions
        out['id']=Train_data
        return out
