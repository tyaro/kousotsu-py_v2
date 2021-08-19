import redis
import json
import pandas as pd
from pandas import json_normalize
import datetime
from DBUtil3 import *

def CalcCRRatioMA(client):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('UP/DOWN比率の移動平均を計算します。')
    query = 'select * from TECHNICAL_UDRATIO order by calcTime desc limit 150'

    
    df = pd.read_sql_query(query,con=ENGINE)
    df = df.iloc[::-1]
    dfSMA5 = df.rolling(window=5,center=False).mean()
    dfSMA5 = round(dfSMA5,2).astype(str)
    dfSMA15 = df.rolling(window=15,center=False).mean()
    dfSMA15 = round(dfSMA15,2).astype(str)
    dfSMA30 = df.rolling(window=30,center=False).mean()
    dfSMA30 = round(dfSMA30,2).astype(str)
    dfSMA60 = df.rolling(window=60,center=False).mean()
    dfSMA60 = round(dfSMA60,2).astype(str)
    dfEMA5 = df.ewm(span=5,adjust=False).mean()
    dfEMA5 = round(dfEMA5,2).astype(str)
    dfEMA15 = df.ewm(span=15,adjust=False).mean()
    dfEMA15 = round(dfEMA15,2).astype(str)
    dfEMA30 = df.ewm(span=30,adjust=False).mean()
    dfEMA30 = round(dfEMA30,2).astype(str)
    dfEMA60 = df.ewm(span=60,adjust=False).mean()
    dfEMA60 = round(dfEMA60,2).astype(str)
    dfTrend = df.tail(30).astype(str)

    calcList = {
        'SMA5':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfSMA5.tail(30).to_dict(orient='list')},
        'SMA15':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfSMA15.tail(30).to_dict(orient='list')},
        'SMA30':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfSMA30.tail(30).to_dict(orient='list')},
        'SMA60':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfSMA60.tail(30).to_dict(orient='list')},
        'EMA5':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfEMA5.tail(30).to_dict(orient='list')},
        'EMA15':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfEMA15.tail(30).to_dict(orient='list')},
        'EMA30':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfEMA30.tail(30).to_dict(orient='list')},
        'EMA60':{'Value':dfSMA5.iloc[-1].to_dict(),'Trend':dfEMA60.tail(30).to_dict(orient='list')},
    }

    redisKey = 'UDRatio_'
    for key in calcList:
        redisKey2 = redisKey + key + '_' + 'Value'
        value = calcList[key]['Value']
        setRedis(client,redisKey2,value)
        redisKey3 = redisKey + key + '_' + 'Trend'
        value = calcList[key]['Trend']
        setRedis(client,redisKey3,value)

    return 

def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)
    #print(key,value)



def main():

    client = redis.Redis(host='redis',port=6379,db=0)

    CalcCRRatioMA(client)


if __name__ == "__main__":
    main()