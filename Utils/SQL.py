import csv
import pypyodbc
import json
import Progress_Bar
import setting
from kusto_client import KustoClient
def readCSV(file_path):
    res = []
    with open(file_path, 'r') as f:
        spamreader = csv.reader(f)
        for row in spamreader:
            if len(row) == 0:
                continue
            res.append(row)
    return res


#upload the result to wanjian's SQL
def upload(file):

    db_host = 'asgvm-040'
    db_name = 'WanjiaDB'
    db_user = 'a4xwriter'
    db_pswd = 'fjeu09re'
    connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_pswd
    db = pypyodbc.connect(connection_string, autocommit=True)
    print "...create TMP_CoX_Sessions"

    SQL = '''
            CREATE TABLE TMP_CoX_Sessions (
            SessionId nvarchar(36) PRIMARY KEY,
            Anid nvarchar(128),
            ts_StartTime datetimeoffset(7),
            device_ssid nvarchar(36),
            AResult nvarchar(256),
            AResultTag nvarchar(36),
            Speaker_Side nvarchar(6),
            Wifi_Name nvarchar(64),
            AppInfo_Version nvarchar(36),
            OOBEDevice_Version nvarchar(84),
            OOBEDevice_Id nvarchar(32),
            LogSequence varchar(512),
            TransferToken nvarchar(128)
            );
        '''
    try:
        db.cursor().execute(SQL)
    except pypyodbc.ProgrammingError as e:
        SQL = '''
                DROP TABLE dbo.TMP_CoX_Sessions
            '''
        db.cursor().execute(SQL)
        db.cursor().close()
        db.close()
    print "...create TMP_CoX_Sessions successfully"
    print "...insert data into TMP_CoX_Sessions"
    print "...total sqls : {0}", len(file)
    vall=lambda lst,sz:[lst[i:i+sz] for i in range(0,len(lst),sz)]
    filelst=vall(file,999)
    bar=Progress_Bar.AnimatedProgressBar(100,80)
    for _fileindex in range(len(filelst)):
        _file=filelst[_fileindex]
        vals = []
        bar.progress=(_fileindex+1)*100.0/len(filelst)
        for i in range(len(_file)):
            line = [x.encode('utf-8', 'ignore') for x in _file[i]]

            try:
                # SQL = '''INSERT INTO TMP_CoX_Sessions(SessionId, Anid, ts_StartTime,device_ssid,TransferToken,AResultTag,AppInfo_Version,OOBEDevice_Version,OOBEDevice_Id,AResult,LogSequence,)
                #     VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');
                #     '''.format(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8],
                #                line[9].replace('\'', '\'\''),line[10])
                val = '''(N'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')'''.format(line[0], line[1], line[2], line[3], line[9].replace('\'', '\'\''), line[5], line[12], line[11].replace('\'', '\'\''), line[6],
                               line[7], line[8],line[10],line[4])
            except:
                print line
                raise
            vals.append(val)
        vals=','.join(vals)
        vals=vals+';'
        SQL='''
        INSERT INTO TMP_CoX_Sessions(SessionId, Anid, ts_StartTime,device_ssid,AResult,AResultTag,Speaker_Side,Wifi_Name,AppInfo_Version,OOBEDevice_Version,OOBEDevice_Id,LogSequence,TransferToken) VALUES
        '''+vals
        try:
            db.cursor().execute(SQL)
        except pypyodbc.ProgrammingError as e:
            print SQL
            SQL = '''
                        DROP TABLE dbo.TMP_CoX_Sessions
                    '''
            db.cursor().execute(SQL)
            db.cursor().close()
            db.close()
            raise e
        bar.show_progress()
    print "...insert data into TMP_CoX_Sessions successfully"
    print "...merge TMP_CoX_Sessions with CoXSessions"

    SQL = '''
        MERGE dbo.CoXSessions AS d
        USING dbo.TMP_CoX_Sessions AS dd
        ON (d.SessionId = dd.SessionId)
        WHEN MATCHED THEN UPDATE SET d.Anid=dd.Anid, d.ts_StartTime=dd.ts_StartTime,d.device_ssid=dd.device_ssid, d.TransferToken=dd.TransferToken, d.AResultTag=dd.AResultTag,d.AppInfo_Version=dd.AppInfo_Version,d.OOBEDevice_Version=dd.OOBEDevice_Version,d.OOBEDevice_Id=dd.OOBEDevice_Id,d.AResult=dd.AResult,d.LogSequence=dd.LogSequence, d.Wifi_Name=dd.Wifi_Name,d.Speaker_Side=dd.Speaker_Side
        WHEN NOT MATCHED THEN
            INSERT (SessionId,Anid,ts_StartTime,device_ssid,TransferToken,AResultTag,AppInfo_Version,OOBEDevice_Version,OOBEDevice_Id,AResult,LogSequence,Wifi_Name,Speaker_Side)
                VALUES(dd.SessionId,dd.Anid,dd.ts_StartTime,dd.device_ssid,dd.TransferToken,dd.AResultTag,dd.AppInfo_Version,dd.OOBEDevice_Version,dd.OOBEDevice_Id,dd.AResult,dd.LogSequence,dd.Wifi_Name,dd.Speaker_Side)
            ;
    '''
    db.cursor().execute(SQL)
    print "...merge TMP_CoX_Sessions with CoXSessions successfully"
    print "...drop TMP_CoX_Sessions"

    SQL = '''
        DROP TABLE dbo.TMP_CoX_Sessions
    '''
    db.cursor().execute(SQL)
    print "...drop TMP_CoX_Sessions successfully"
    db.cursor().close()
    db.close()

#download session from kusta
def download(query):
    #use wanjian's c# at present
    pass
if __name__ == '__main__':
    with open(setting.RESULT_PATH + '\\result.json') as f:
        file = json.load(f)
    upload(file)
