import re
from time import strptime,strftime
class LogBase(object):
    # def __init__(self,Message,time):
    #     self.Message=Message
    #     try:
    #         t = strptime(time, '%m/%d/%Y %I:%M:%S %p')
    #         time = strftime("%m/%d/%Y %H:%M:%S", t)
    #     except:
    #         raise BaseException("doesn't match")
    #     self.time=time
    #     self.type=-1
    # id=None
    def setType(self,type):
        self.type=type
    def getId(self):
        raise NotImplementedError("must implement getId method")
