import pypyodbc
from collections import defaultdict,deque
def pull_query(query):
    db_host = 'asgvm-040'
    db_name = 'WanjiaDB'
    db_user = 'a4xwriter'
    db_pswd = 'fjeu09re'
    connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_pswd
    db = pypyodbc.connect(connection_string, autocommit=True)
    try:
        data=db.cursor().execute(query).fetchall()
    except BaseException as e:
        print e
        db.cursor().close()
        db.close()
        return None
    db.cursor().close()
    db.close()
    return data


def pull_LogSequence():
    query='''
        select LogSequence
        from CoXSessions
        where AppInfo_Version like '2.3.%' or AppInfo_Version like '2.4.%' or AppInfo_Version like '2.2.%' and LogSequence!=''
    '''
    data=pull_query(query)
    return data

#used by get_patterns
def _window(seq,n):
    it=iter(seq)
    win=deque((next(it,'') for _ in range(n)),maxlen=n)
    yield win
    append=win.append
    for e in it:
        append(e)
        yield win


#use 3-gram to transfet log sequence to word
def get_patterns():
    data=pull_LogSequence()
    wordbag=defaultdict(int)
    for (seq,) in data:
        if seq==None:
            continue
        seq=list(seq)
        for word in _window(seq,3):
            try:
                wordbag[''.join(word)]+=1
            except:
                break
    return wordbag


if __name__=='__main__':
    print 'finish'
