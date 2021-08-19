from DBUtil3 import *
import redis
import pandas as pd
import json
from VRank import VolumeRanking

def getVolumeData(client,redisKey,tableName,pair,span):

    s = tableName.replace('BINANCE_KLINES_','')

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    min = datetime.datetime.now().minute
    hour = (datetime.datetime.now()+datetime.timedelta(hours=-9)).hour

    k = 0
    if s == '15MIN':
        modMin = min % 15
        k = modMin/15
    if s == '1HOUR':
        modMin = min % 60
        k = modMin/60
    if s == '4HOUR':
        modHour = hour/4
        modMin = min % 60
        k = modMin/60 + modHour/4
    if s == '6HOUR':
        modHour = hour/6
        modMin = min % 60
        k = modMin/60 + modHour/6
    if s == '1DAY':
        modHour = hour/24
        modMin = min % 60
        k = modMin/60 + modHour/24

    query = 'select openTime,symbol,usdtVolume,takerBuyUsdtVolume from %s where symbol="%s" order by openTime desc limit %s'
    query1 = query % (tableName,pair,span)
    df = pd.read_sql_query(query1,con=ENGINE)
    df = df.iloc[::-1]


    # 最終行削除したもので平均などは計算
    dfCalc = df[:-1].copy()

    PV = df.usdtVolume.iloc[-1] # 実PV
    if(modMin>0):
        PVC = PV / k # 演算値PV
    else:
        PVC = PV

    # 変更
    #PV = dfCalc.usdtVolume.iloc[-1] # 一個前
    #PVC=PV

    AVG = dfCalc.usdtVolume.mean()
    STD = dfCalc.usdtVolume.std()
    MED = dfCalc.usdtVolume.median()
    DV = (PVC-AVG)*10/STD + 50 #現在ボリュームの偏差値
    RATE = PVC/MED*100
    df['Ratio'] = round(df.takerBuyUsdtVolume/df.usdtVolume*100,2)
    RATIO = df.Ratio.iloc[-1]

    TREND = df.usdtVolume.tail(span).astype(str).to_list()
    TREND2 = df.Ratio.tail(span).astype(str).to_list()

    # 変更
    #print(dfCalc)
    #dfCalc['Ratio'] = round(dfCalc.takerBuyUsdtVolume/dfCalc.usdtVolume*100,2)
    #RATIO = dfCalc.Ratio.iloc[-1]
    #TREND = dfCalc.usdtVolume.tail(span-1).astype(str).to_list()
    #TREND2 = dfCalc.Ratio.tail(span-1).astype(str).to_list()

    info = {
        'Pair':pair,
        'PV':str(round(PV,2)),
        'PVC':str(round(PVC,2)),
        'AVG':str(round(AVG,2)),
        'MED':str(round(MED,2)),
        'DV':str(round(DV,2)),
        'RATE':str(round(RATE,2)),
        'RATIO':str(round(RATIO,2)),
        'SPAN':span,
        'calcTime':now,
    }

    redisKey2 = redisKey + '_' + pair + '_' + s
    redisKey3 = redisKey2 + '_Trend'
    redisKey4 = redisKey2 + '_Trend_Ratio'
    #print(PV,calcPV,AVG,MED,DV,dfCalc)
    #print(info)
    setRedis(client,redisKey2,info)
    setRedis(client,redisKey3,TREND)
    setRedis(client,redisKey4,TREND2)

    return info

def VolumeEvaluation(client):
    print('出来高を解析します。')

    symbolList = GetSymbolList()
    redisKey = 'Volume_Info'

    calcList15M = []
    calcList1H = []
    calcList4H = []
    calcList6H = []
    calcList1D = []
    # 全銘柄(Volume)を取得
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]

        span = 4*24+1

        list15M = getVolumeData(client,redisKey,'BINANCE_KLINES_15MIN',pair,span)
        list1H = getVolumeData(client,redisKey,'BINANCE_KLINES_1HOUR',pair,24*7+1)
        list4H = getVolumeData(client,redisKey,'BINANCE_KLINES_4HOUR',pair,6*20+1)
        list6H = getVolumeData(client,redisKey,'BINANCE_KLINES_6HOUR',pair,4*30+1)
        list1D = getVolumeData(client,redisKey,'BINANCE_KLINES_1DAY',pair,31)

        calcList15M.append(list15M)
        calcList1H.append(list1H)
        calcList4H.append(list4H)
        calcList6H.append(list6H)
        calcList1D.append(list1D)
        
    #print(calcList)
    setRedis(client,redisKey+'_15MIN',calcList15M)
    setRedis(client,redisKey+'_1HOUR',calcList1H)
    setRedis(client,redisKey+'_4HOUR',calcList4H)
    setRedis(client,redisKey+'_6HOUR',calcList6H)
    setRedis(client,redisKey+'_1DAY',calcList1D)

def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)
    #client.delete(key)
    #print(key,value)

def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    VolumeEvaluation(client)
    VolumeRanking(client)

if __name__=="__main__":
    main()
