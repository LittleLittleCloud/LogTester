import json
import requests
from base64 import b64encode
from pandas import DataFrame
APIURL = "https://kusto.aria.microsoft.com/v1/rest/query"
def _pull(tenant, token, query):
    ten_token = b64encode("{0}:{1}".format(tenant, token))
    h = {
        "x-ms-user": "FAREAST\\t-zhaxia",
        "content-type": "application/json",
        "Authorization": "Basic {0}".format(ten_token)
    }
    d = {
        "csl": query,
        "db": tenant,
        "properties": {
            "ClientEndpoint": None,
            "DataEngine": 0,
            "DebugMode": False,
            "DisableParallelization": False,
            "EchoQueryMode": False,
            "EnablePrejoinFilters": False,
            "Id": None,
            "JoinStrategy": 0,
            "ProfileIterationCount": 20,
            "ProfileMode": False,
            "StagedQuery": True,
            "User": None,
        }
    }
    res = requests.post(APIURL, headers=h, data=json.dumps(d))
    return res

def _parseData(data):
    colInfo = data["Tables"][0]["Columns"]
    colNames = [x["ColumnName"].encode("utf-8", "") for x in colInfo]
    colTypes = [x["DataType"] for x in colInfo]
    res=[]
    for row in data["Tables"][0]["Rows"]:
        try:
            tmp=map(lambda x:''if x ==None else x.encode("utf-8",""),row)
            res.append(tmp)
        except AttributeError as e:
            print e,row
            pass
    return DataFrame(res, columns=colNames)