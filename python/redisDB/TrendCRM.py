import json
import redis
from DBUtil3 import *



def setRedis(client,key,redisData):
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)

def GetCRMTrendData(client):
    query = 'select * from TECHNICAL_CRM order by calcTime desc limit 1500'

    df = pd.read_sql_query(query,con=ENGINE)
    df = df.iloc[::-1]
    dfSMA05 = df.rolling(window=5,center=False).mean()
    dfSMA15 = df.rolling(window=15,center=False).mean()
    dfSMA30 = df.rolling(window=30,center=False).mean()
    dfSMA60 = df.rolling(window=60,center=False).mean()
    dfSMA240 = df.rolling(window=240,center=False).mean()
    dfSMA360 = df.rolling(window=360,center=False).mean()
    dfEMA05 = df.ewm(span=5,adjust=False).mean()
    dfEMA15 = df.ewm(span=15,adjust=False).mean()
    dfEMA30 = df.ewm(span=30,adjust=False).mean()
    dfEMA60 = df.ewm(span=60,adjust=False).mean()
    dfEMA240 = df.ewm(span=240,adjust=False).mean()
    dfEMA360 = df.ewm(span=360,adjust=False).mean()

    df = df.drop('calcTime',axis=1)
    df = df.astype(str)
    dfSMA05 = round(dfSMA05,2).astype(str)
    dfSMA15 = round(dfSMA15,2).astype(str)
    dfSMA30 = round(dfSMA30,2).astype(str)
    dfSMA60 = round(dfSMA60,2).astype(str)
    dfSMA240 = round(dfSMA240,2).astype(str)
    dfSMA360 = round(dfSMA360,2).astype(str)
    dfEMA05 = round(dfEMA05,2).astype(str)
    dfEMA15 = round(dfEMA15,2).astype(str)
    dfEMA30 = round(dfEMA30,2).astype(str)
    dfEMA60 = round(dfEMA60,2).astype(str)
    dfEMA240 = round(dfEMA240,2).astype(str)
    dfEMA360 = round(dfEMA360,2).astype(str)

    calcList = {
        'PV':df.tail(960).to_dict(orient='list'),
        'SMA05':dfSMA05.tail(960).to_dict(orient='list'),
        'SMA15':dfSMA15.tail(960).to_dict(orient='list'),
        'SMA30':dfSMA30.tail(960).to_dict(orient='list'),
        'SMA60':dfSMA60.tail(960).to_dict(orient='list'),
        'SMA240':dfSMA240.tail(960).to_dict(orient='list'),
        'SMA360':dfSMA360.tail(960).to_dict(orient='list'),
        'EMA05':dfEMA05.tail(960).to_dict(orient='list'),
        'EMA15':dfEMA15.tail(960).to_dict(orient='list'),
        'EMA30':dfEMA30.tail(960).to_dict(orient='list'),
        'EMA60':dfEMA60.tail(960).to_dict(orient='list'),
        'EMA240':dfEMA240.tail(960).to_dict(orient='list'),
        'EMA360':dfEMA360.tail(960).to_dict(orient='list'),
    }

    redisKey = 'CRMTrend_'
    for calcType in calcList:
        redisKey2 = redisKey + calcType + '_'
        for span in calcList[calcType]:
            redisKey3 = redisKey2 + span
            value = calcList[calcType][span]
            #print(redisKey3,value)
            setRedis(client,redisKey3,value)

def main():

    client = redis.Redis(host='redis',port=6379,db=0)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    GetCRMTrendData(client)


if __name__ == "__main__":
    print('変動率中央値のトレンドを生成します。')
    main()
