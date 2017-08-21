#Readme.txt

LogTester is a module written in python in order to convenient the construciotn of universal Log Analyzer. with the help of this module, theoratically, you can build whatever Log analyzer (basd on Session construction) you want with relatively few code.

the structure of this module is listed below

.LogTester
-Utils #provide some tools to facilitate CoA and CoI 
-AnomalyDetectPlugin #Plugin that provide anomaly detect function
-Base                #provide PluginBase class
-ClassifyPlugin      
-FeaturePlugin       #Plugin that provide feature2vec function
-InputPlugin         
-PreprocessPlugin    
-PostprocessPlugin
-PrepareTrainPlugin  #Plugin that prepare train data
-Session             #provide SessionBase class that you must implement
-Log                 #provide LogBase class that you must implement
-shell               #provide shellBase class that you can choose to re-implement or not

In common, an entire process in handling the Log can be viewed as a pipeline, where each process is relatively independent. for example, in CoX LogTester, the train pipeline is defined like this:

PrepareTrain ===> Input ===> Feature ===> Classify ===> AnomalyDetect ===> Postprocess

next, a step-by-step tutorial on how to build your own Log Analyzer will be provide, the full code can be found in the sub dir "biaji"


firstly, you should new a setting.py file in the project, the name should not be motified for the LogTester module will load this file to do some initialize work.
you can copy the content from setting_t.py to setting.py, and rename the variables. after doing that step, run this script to finish initialization
after finishing initialization, a few dir will be built, put your traindata.xml to tranSet, and patterns.json to Pattern.  traindate.xml  