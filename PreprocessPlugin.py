import numpy as np
import json
from Base import PluginBase
from xml.dom import minidom
from LogTester.Utils import File
from LogTester.Utils.Extract import extractSessions
import setting
class PreprocessPlugin(PluginBase):
    pipe_In = {'Sessions_path':str,'Token_path':str}
    pipe_Out = {'id': list}
    def _extractSessions(self,**args):
        return extractSessions(source=args['source'],filename=args['today_session'])
    def fit(self,In,y=None,**args):
        return self
    def transform(self,In,**args):
        res=self.fetch(In,Sessions_path=str,Token_path=str)
        Sessions_path=res['Sessions_path']
        Token_path=res['Token_path']
        Sessions=self._extractSessions(source=Sessions_path,today_session=setting.TODAYSESSION_PATH)
        tokens = File.readCSV(Token_path)
        tokensdict = {}
        for x in tokens:
            try:
                tokensdict[x[0]] = (x[2], x[1])
            except IndexError:
                pass
        out=In
        out['Sessions']=Sessions
        out['TokenDict']=tokensdict
        out['id']=np.array(Sessions.keys())
        return out