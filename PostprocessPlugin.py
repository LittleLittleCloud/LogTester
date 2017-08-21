import numpy as np
import json
import setting
from Base import PluginBase
from openpyxl import Workbook
import re
class PostprocessPlugin(PluginBase):
    pipe_In = {'SPE':np.ndarray,'res':np.ndarray,'Sessions':dict}
    pipe_Out = {'result.json':int,'report.xlsx':int}
    def __init__(self):
        self.result_path=setting.RESULT_PATH
    def fit(self,In,y,**args):
        return self
    def transform(self,In,**args):
        _res=self.fetch(In,SPE=np.ndarray,res=np.ndarray,Sessions=dict,TokenDict=dict)
        SPE=_res['SPE']
        resVec=_res['res']
        SessionsDic=_res['Sessions']
        Sessions=SessionsDic.values()
        tokens=_res['TokenDict']
        for i in range(0, len(Sessions)):
            try:
                Sessions[i]['OSVersion'] = ''
                Sessions[i]['DeviceInfoID'] = ''
                session = Sessions[i]
                tmpLogs = filter(lambda x: x['type'] == 0, session['logs'])
                Sessions[i]['token'] = ''
                # set Type
                if len(tmpLogs) == 1:
                    token = re.split(r'[:]', tmpLogs[0]['Message'])[-1]
                    Sessions[i]['token'] = token
                    if token in tokens.keys():
                        Sessions[i]['status'] = 0
                        Sessions[i]['OSVersion'] = tokens[token][0]
                        Sessions[i]['DeviceInfoID'] = tokens[token][1]

                    else:
                        Sessions[i]['status'] = -1
            except IndexError:
                print session
            finally:
                pass
        tagMeans = setting.TAG_MEAN
        wb = Workbook()
        ws = wb.active
        ws.append(
            ['time', 'SessionID', 'error info', 'feature', 'speaker name', 'wifi name', 'speaker side', 'anid', 'token',
             'OSVersion', 'AppVersion', 'Sureness'])

        suc_ = []
        for i in range(len(Sessions)):
            x = Sessions[i]
            logs = x['logs']
            time = logs[0]['time']

            suc = []
            suc.append(x['id'])  # 0
            suc.append(x['ansid'])  # 1
            suc.append(time)  # 2

            speakerName = ''

            wifiName = ''
            for log in logs:
                if 'CRTCAOobeConfigWifiViewWAC started, accessory name' in log['Message']:
                    speakerName = log['Message'].split(':')[-1]
                if 'wifiname' in log['Message']:
                    wifiName = log['Message'].split(':')[-1]
                if '169.254' in log['Message']:
                    # auto IP
                    if x['status'] != 0:
                        resVec[i] = 4
            if resVec[i] != x['status']:
                if resVec[i] == 2 and x['status'] != 0:
                    resVec[i] = 20
                if resVec[i] == 1 and x['status'] == 0:
                    resVec[i] = 21
                # print "fail prediction on SessionID: "+x['id']+" is ",res," with feature "+''.join(x['feature'])+" speakerName: "+speakerName+" wifiNmae: "+wifiName
                row = [time, x['id'], tagMeans[resVec[i]], ''.join(x['feature']), speakerName, wifiName,
                       x['status'] == 0, x['ansid'], x['token'], x['OSVersion'], x['appversion'], SPE[i]]
            else:
                row = [time, x['id'], tagMeans[resVec[i]], ''.join(x['feature']), speakerName, wifiName,
                       x['status'] == 0, x['ansid'], x['token'], x['OSVersion'], x['appversion'], SPE[i]]
            ws.append(row)
            suc.append(speakerName)  # 3
            suc.append(x['token'])  # 4
            if resVec[i] in [0, 16, 18]:
                suc.append('success')
            elif resVec[i] in [1, 2, 4, 10, 12, 13, 15, 17, 19, 20, 21]:
                suc.append('fail')
            else:
                suc.append('neglect')  # 5
            suc.append(x['appversion'])  # 6
            suc.append(x['OSVersion'])  # 7
            suc.append(x['DeviceInfoID'])  # 8
            suc.append(tagMeans[resVec[i]])  # 9
            suc.append(''.join(x['feature']))  # 10
            suc.append(wifiName)  # 11
            suc.append('TRUE' if x['status'] == 0 else 'FALSE')  # 12
            suc_.append(suc)

        wb.save(self.result_path + '\\report.xlsx')
        print "save file"
        with open(self.result_path + '\\result.json', 'w') as f:
            json.dump(suc_, f)
        out=In
        out['result.json']=suc_
        out['report.xlsx']=wb
        return out
    def predict(self,In,**args):
        return self.transform(In)
    def score(self,In,**args):
        return self.transform(In)
