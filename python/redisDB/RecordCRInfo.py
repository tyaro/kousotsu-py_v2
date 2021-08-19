import redis
import json
import pandas as pd
from pandas import json_normalize
import datetime
from DBUtil3 import *

def TechnicalInfo2db(row,tablename):

    if not row:
        print('データがありません')
        return

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = 'INSERT INTO %s \
            (calctime,\
            UP1M,DOWN1M,HOLD1M,\
            UP5M,DOWN5M,HOLD5M,\
            UP10M,DOWN10M,HOLD10M,\
            UP15M,DOWN15M,HOLD15M,\
            UP30M,DOWN30M,HOLD30M,\
            UP60M,DOWN60M,HOLD60M,\
            UP240M,DOWN240M,HOLD240M,\
            UP360M,DOWN360M,HOLD360M,\
            UP480M,DOWN480M,HOLD480M,\
            UP720M,DOWN720M,HOLD720M,\
            UP1440M,DOWN1440M,HOLD1440M\
            ) \
            VALUES("%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

    query1 = query % (
        tablename,
        now,
        row['1M']['UP'],row['1M']['DOWN'],row['1M']['HOLD'],
        row['5M']['UP'],row['5M']['DOWN'],row['5M']['HOLD'],
        row['10M']['UP'],row['10M']['DOWN'],row['10M']['HOLD'],
        row['15M']['UP'],row['15M']['DOWN'],row['15M']['HOLD'],
        row['30M']['UP'],row['30M']['DOWN'],row['30M']['HOLD'],
        row['60M']['UP'],row['60M']['DOWN'],row['60M']['HOLD'],
        row['240M']['UP'],row['240M']['DOWN'],row['240M']['HOLD'],
        row['360M']['UP'],row['360M']['DOWN'],row['360M']['HOLD'],
        row['480M']['UP'],row['480M']['DOWN'],row['480M']['HOLD'],
        row['720M']['UP'],row['720M']['DOWN'],row['720M']['HOLD'],
        row['1440M']['UP'],row['1440M']['DOWN'],row['1440M']['HOLD']
        )

    ENGINE.execute(query1)
    return

def RecordUDRatio(client):
    print('UP/DOWN比率をDBに登録します')
    key = 'CRMedian'
    value = client.get(key)

    data = json.loads(value)
    TechnicalInfo2db(data['Value']['CNT'],'TECHNICAL_UDRATIO')
    

def main():
    client = redis.Redis(host='redis',port=6379,db=0)
    RecordUDRatio(client)
    

def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)



if __name__ == "__main__":
    main()