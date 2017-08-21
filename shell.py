from cmd2 import Cmd
from ClassifyPlugin import ClassifyPlugin
from FeaturePlugin import FeaturePlugin
from InputPlugin import InputPlugin
from AnomalyDetectPlugin import AnomalyDetectPlugin
from PrepareTrainPlugin import PrepareTrainPlugin
from Utils.Extract import extractSessions,AddNewSessions
from PreprocessPlugin import PreprocessPlugin
from PostprocessPlugin import PostprocessPlugin
from sklearn.model_selection import train_test_split
from Utils.PCA import DrawQ_distrubute
from Utils.Extract import getTrainData
import json
import re
from random import shuffle
from sklearn.externals import joblib
import subprocess
import setting
import Utils
import numpy as np
from sklearn.pipeline import Pipeline
import json

class ShellBase(Cmd,object):


    prompt = '>>>'
    complete_pull=Cmd.path_complete
    complete_analyze=Cmd.path_complete
    complete_update=Cmd.path_complete

    def __init__(self,):
        with open(setting.SESSION_PATH,'r') as f:
            print setting.SESSION_PATH
            self.session=json.load(f)
        Cmd.__init__(self)


    def do_train(self, arg):
        arge = re.split(r'[ ]*', arg)

        try:
            if len(arge) != 1:
                raise BaseException('bad syntax!, only accept 1 arguemnts')
            with open(setting.SESSION_PATH) as f:
                Sessions = json.load(f)
            traindata = getTrainData(Sessions)
            data = traindata
            __y = range(len(data))
            # shuffle(data)
            X_train, X_test, y_train, y_test = train_test_split(data, __y, test_size=float(arge[0]))
            X_train_ = np.array(X_train)
            X = X_train_[:, 0].transpose()
            _y = np.array(map(int, X_train_[:, 1].transpose()))

            print ("data size: ", len(X_train))
            pipeline = Pipeline([
                ('preprocess', PrepareTrainPlugin()),
                ('input', InputPlugin()),
                ('feature', FeaturePlugin()),
                ('svm', ClassifyPlugin(kernel='linear')),
                ('anomaly_detect', AnomalyDetectPlugin())
            ])
            pipeline.fit({'Sessions_path':setting.SESSION_PATH,'id':X}, _y,svm__cache=True)
            if arge[0]!=0.0:
                X_test_ = np.array(X_test)
                X_t = X_test_[:, 0].transpose()
                _y_t = np.array(map(int, X_test_[:, 1].transpose()))
                a = pipeline.score({'Sessions_path': setting.SESSION_PATH, 'id': X_t}, _y_t)
                print 'accuracy: {0}'.format(a['predict_accuracy'])
                print 'anomaly_detect_accuracy: {0}'.format(a['anomaly_detect_accuracy'])
                print 'anomaly_detect_recall: {0}'.format(a['anomaly_detect_recall'])
        except NameError:
            pass
        except EOFError:
            pass
        finally:
            pass
    def do_analyze(self,args):
        args=re.split(r'[ ]*',args)

        try:
            if len(args)!=2:
                raise BaseException('bad syntax!, only accept 2 arguemnts')
            SVM=joblib.load(setting.MODEL_PATH+'\\SVM')
            testpipeline = Pipeline([
                ('preprocess', PreprocessPlugin()),
                ('input', InputPlugin()),
                ('feature', FeaturePlugin()),
                ('svm', SVM),
                ('anomaly_detect', AnomalyDetectPlugin()),
                ('output', PostprocessPlugin())
            ])
            testpipeline.predict({'Sessions_path':args[0],'Token_path':args[1]})
        except BaseException as e:
            print e
        finally:
            pass
    def do_pull(self,arge):
        raise NotImplementedError("do_pull not implement")
    def do_update(self,arg):
        args=re.split(r'[ ]*',arg)
        try:
            if len(args)!=1:
                raise BaseException("bad syntax!, only accept 1 arguemnts")
            AddNewSessions(args[0])
            print "finish update Sessions"
        except BaseException as e:
            print e
            pass
    def do_search(self,arg):
        args=re.split(' ',arg)
        try:
            if len(args)!=1:
                raise BaseException("bad syntax!, only accept 1 arguemnts")
            print ''.join(self.session[args[0]]['feature'])
        except KeyError:
            print "don't have that key"
            pass
        except BaseException as e:
            print e
            pass

    def do_showtags(self,arg):
        try:
            if arg!='':
                raise BaseException("bad syntax!, only accept 0 arguemnts")
            tagMeans=setting.TAG_MEAN
            for x in tagMeans:
                print [x,tagMeans[x]]
        except BaseException as e:
            print e
    def do_change_q(self,arg):
        args=re.split(r'[ ]*',arg)
        try:
            if len(args)!=2:
                raise BaseException("bad syntax!, only accept 2 arguemnts")
            type=int(args[0])
            val=int(args[1])
            SetQ_val(type,val)

        except BaseException as e:
            print e
            pass
    def do_draw_q_distribution(self,arg):
        args = re.split(r'[ ]*', arg)
        try:
            if len(args) != 1:
                raise BaseException("bad syntax!, only accept 1 arguemnts")
            N=1000
            c=2.65
            r=0.9
            type=int(args[0])
            DrawQ_distrubute(N,c,r,type)
        except BaseException as e:
            print e
            pass
    def do_upload(self,arg):
        try:
            with open(setting.RESULT_PATH + '\\result.json') as f:
                file = json.load(f)
            Utils.SQL.upload(file)
        except BaseException as e:
            print e
            pass


