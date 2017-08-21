class SessionBase:
    def addLog(self,Log):
        self.logs.append(Log)
    def sort(self):
        self.logs.sort(key=lambda x:x.time)
    def calcFeature(self):
        raise NotImplementedError("must implement calcFeature method")
    def setStatus(self,i):
        self.status=i

    def __dict__(self):
        raise NotImplementedError("must implement __dict__ method")

    def update(self,log):
        raise NotImplementedError("must implement update method")
