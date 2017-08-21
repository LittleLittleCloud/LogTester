import SQL
import LogTester.Utils
import sys
import json
from Session import Session
from Log import Log
from setting import setTypeOfLogs
import setting
from LogTester import Utils
from xml.dom import minidom
from collections import defaultdict

def extractSessions(source, filename=None):
    Sessons=Utils.File.readCSV(source)
    tmp={}
    logs=[]
    print('...start to extract data')
    for row in Sessons:
        try:
            tmpLog=Log(row)
            tmpLog.setType(setTypeOfLogs(tmpLog.Message))
            logs.append(tmpLog)
        except BaseException as e:
            print e
            pass
    Sessions={}
    for log in logs:
        id=log.getId()
        if id in Sessions:
            Sessions[id].update(log)
        else:
            Sessions[id]=Session(id)
            Sessions[id].update(log)
    print('...start to calc features')
    for x in Sessions:
        Sessions[x].calcFeature()
    if filename!=None:
        print ('...start to save session to {0}'.format(filename))
        with open(filename,'w') as f:
            json.dump(Sessions,f,default=lambda x:x.__dict__)
    print('...finish')
    return json.loads(json.dumps(Sessions,default=lambda x:x.__dict__))

def AddNewSessions(source):
    newSessions=extractSessions(source)
    with open(setting.SESSION_PATH,'r') as f:
        Sessions = json.load(f)
    for session in newSessions:
        Sessions[session]=newSessions[session]
        print "update session:" + session
    with open(setting.SESSION_PATH,'w') as f:
        json.dump(Sessions,f,default=lambda x:x.__dict__)
    return


def getTrainData(Sessions):
    traindata=[]
    xmldoc=minidom.parse(setting.TRAINDATA_PATH)
    itemlist=xmldoc.getElementsByTagName('item')
    for item in itemlist:
        ID=item.attributes['SessionID'].value
        type=int(item.childNodes[0].data)
        if ID in Sessions:
            traindata.append([ID,type])
    return traindata
if __name__=='__main__':
    if len(sys.argv)==2:
        source=sys.argv[1]
        AddNewSessions(source)

    if len(sys.argv)==3:
        source=sys.argv[1]
        path=sys.argv[2]
        extractSessions(source,path)
    if len(sys.argv)==1:
        with open(setting.SESSION_PATH,'r') as f:
            Sessions=json.load(f)
        while True:
            print "input yout session id:"
            SessionID=raw_input()
            try:
                print ''.join(Sessions[SessionID]['feature'])
            except KeyError:
                print "don't have that key"
            finally:
                pass