import redis
import json
import pandas as pd
from pandas import json_normalize
import datetime
from DBUtil3 import *
from RecordCRInfo import RecordUDRatio
from TrendCRRatio import CalcCRRatioMA
from TrendCRM import GetCRMTrendData

def calc(span,df):
    colName = 'CRate' + span
    colName2 = 'DEV' + span
    MED = round(df[colName].astype(float).median(),2)
    AVG = df[colName].astype(float).mean()
    STD = df[colName].astype(float).std()
    up = df[colName].astype(float) > 0
    down = df[colName].astype(float) < 0
    stay = df[colName].astype(float) == 0
    NumUp = str(up.sum())
    NumDown = str(down.sum())
    NumStay = str(stay.sum())
    
    df[colName2] = round((df[colName].astype(float)-AVG)*10/STD + 50,2)
    AVG = round(AVG,2)
    STD = round(STD,2)
    return MED,AVG,STD,NumUp,NumDown,NumStay,df

def TechnicalInfo2db(row,tablename):

    if not row:
        return

    query = 'INSERT INTO %s \
            (calctime,MED01,MED05,MED10,MED15,MED30,MED60,MED240,MED360,MED480,MED720,MED1440) \
            VALUES("%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

    query1 = query % (
        tablename,
        row['calcTime'],
        row['Value']['1M'],
        row['Value']['5M'],
        row['Value']['10M'],
        row['Value']['15M'],
        row['Value']['30M'],
        row['Value']['60M'],
        row['Value']['240M'],
        row['Value']['360M'],
        row['Value']['480M'],
        row['Value']['720M'],
        row['Value']['1440M'],
        )

    ENGINE.execute(query1)
    
    return

def setRedisMedian(client,value):
    key = 'CRMedian'
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)

def setRedisDeviationValue(client,value):
    key = 'DeviationValue'
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)


def setRedisDeviationValue2(client,value,symbolName):
    key = 'DeviationValue_' + symbolName
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)

def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'CR_Future'
    value = client.get(key)
    data = json.loads(value)
    df = json_normalize(data)
    #df1 = df[df.pair=='BTCDOMUSDT']
    #print(df1)
    df = df[df.pair!='BTCDOMUSDT']
    df = df.drop('price.Value',axis=1)
    df = df.drop('price.Trend',axis=1)
    df = df.drop('point',axis=1)
    df.calcTime = now

    MED01,AVG01,STD01,NU01,ND01,NS01,df = calc('01',df)
    MED05,AVG05,STD05,NU05,ND05,NS05,df = calc('05',df)
    MED10,AVG10,STD10,NU10,ND10,NS10,df = calc('10',df)
    MED15,AVG15,STD15,NU15,ND15,NS15,df = calc('15',df)
    MED30,AVG30,STD30,NU30,ND30,NS30,df = calc('30',df)
    MED60,AVG60,STD60,NU60,ND60,NS60,df = calc('60',df)
    MED240,AVG240,STD240,NU240,ND240,NS240,df = calc('240',df)
    MED360,AVG360,STD360,NU360,ND360,NS360,df = calc('360',df)
    MED480,AVG480,STD480,NU480,ND480,NS480,df = calc('480',df)
    MED720,AVG720,STD720,NU720,ND720,NS720,df = calc('720',df)
    MED1440,AVG1440,STD1440,NU1440,ND1440,NS1440,df = calc('1440',df)


    #print(MED01,MED05,MED30,MED60,MED240,MED360,MED480,MED720)
    
    medianData = {
        'Status': 'Change Rate Median',
        'Value':{
            '1M':MED01,
            '5M':MED05,
            '10M':MED10,
            '15M':MED15,
            '30M':MED30,
            '60M':MED60,
            '240M':MED240,
            '360M':MED360,
            '480M':MED480,
            '720M':MED720,
            '1440M':MED1440,
        },
        'calcTime':now,
    }
    redisMedianData = {
        'Status': 'Change Rate Median',
        'Value':{
            'CRM':{
                '1M':str(MED01),
                '5M':str(MED05),
                '10M':str(MED10),
                '15M':str(MED15),
                '30M':str(MED30),
                '60M':str(MED60),
                '240M':str(MED240),
                '360M':str(MED360),
                '480M':str(MED480),
                '720M':str(MED720),
                '1440M':str(MED1440),
            },
            'AVG':{
                '1M':str(AVG01),
                '5M':str(AVG05),
                '10M':str(AVG10),
                '15M':str(AVG15),
                '30M':str(AVG30),
                '60M':str(AVG60),
                '240M':str(AVG240),
                '360M':str(AVG360),
                '480M':str(AVG480),
                '720M':str(AVG720),
                '1440M':str(AVG1440),
            },
            'STD':{
                '1M':str(STD01),
                '5M':str(STD05),
                '10M':str(STD10),
                '15M':str(STD15),
                '30M':str(STD30),
                '60M':str(STD60),
                '240M':str(STD240),
                '360M':str(STD360),
                '480M':str(STD480),
                '720M':str(STD720),
                '1440M':str(STD1440),
            },
            'CNT':{
                '1M':{'UP':NU01,'DOWN':ND01,'HOLD':NS01},
                '5M':{'UP':NU05,'DOWN':ND05,'HOLD':NS05},
                '10M':{'UP':NU10,'DOWN':ND10,'HOLD':NS10},
                '15M':{'UP':NU15,'DOWN':ND15,'HOLD':NS15},
                '30M':{'UP':NU30,'DOWN':ND30,'HOLD':NS30},
                '60M':{'UP':NU60,'DOWN':ND60,'HOLD':NS60},
                '240M':{'UP':NU240,'DOWN':ND240,'HOLD':NS240},
                '360M':{'UP':NU360,'DOWN':ND360,'HOLD':NS360},
                '480M':{'UP':NU480,'DOWN':ND480,'HOLD':NS480},
                '720M':{'UP':NU720,'DOWN':ND720,'HOLD':NS720},
                '1440M':{'UP':NU1440,'DOWN':ND1440,'HOLD':NS1440},
            },
        },
        'calcTime':now,
    }
    TechnicalInfo2db(medianData,'TECHNICAL_CRM')
    setRedisMedian(client,redisMedianData)
    df= df.astype(str)
    calcList = df.to_dict(orient='records')
    setRedisDeviationValue(client,calcList)

    for row in calcList:
        pair = row['pair']
        setRedisDeviationValue2(client,row,pair)

    RecordUDRatio(client)
    CalcCRRatioMA(client)
    GetCRMTrendData(client)

if __name__ == "__main__":
    print('変動率を分析します')
    main()
