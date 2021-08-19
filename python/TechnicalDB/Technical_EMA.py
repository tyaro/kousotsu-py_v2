import pandas as pd
from const import *
from DBUtil2 import *
import datetime
import json
import redis

# EMAの計算
# データフレームに新規列(項目名:colName)を作成しspanで指定したEMAを入れる
# 引数で渡すデータフレームはローソク足データを想定
def CalcEMA(df,span,colName,point):
    # 終値を指定期間でEMA計算。1行で出来るとかすげーわ
    df[colName] = round(df[CLOSE_].ewm(span=span,adjust=False).mean(),point)

    # デバッグ用
    #print(df.loc[:,['openTime','close','EMA']])

    return df  

def CalcEMABTC(df,span,colName):
    # 終値を指定期間でEMA計算。1行で出来るとかすげーわ
    df[colName] = df[CLOSE_].ewm(span=span,adjust=False).mean()
    df[colName] = df[colName].map('{:.8f}'.format)
    # デバッグ用
    #print(df.loc[:,['openTime','close','EMA']])

    return df  
def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # シンボルリストをDBから取得
    symbolList = GetSymbolList()

    # テクニカル演算のリストを作成
    calcList = []
    redisData = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]
 
        # Tickerデータとローソク足データを取得
        dfTicker = GetTickerData('BINANCE_TICKER_INFO',pair,5)
        dfBTCTicker = GetTickerData('BINANCE_TICKER_INFO_SPOT_BTC',btcPair,5)
        df1Day = GetKlinesData('BINANCE_KLINES_1DAY',pair,500)
        df1DayBTC = GetKlinesData('BINANCE_KLINES_1DAY_BTC',btcPair,500)

        #print(dfBTCTicker)
        #最終価格取得
        lastPrice = dfTicker.price.iloc[-1]
        lastPriceBTC = 0.0
        if len(dfBTCTicker) > 3:
            lastPriceBTC = dfBTCTicker.price.iloc[-1]
            df1DayBTC.Close.iloc[-1] = lastPriceBTC

        # ローソク足データの最終行の終値に現在価格を入れる
        df1Day.Close.iloc[-1] = lastPrice

        df1DayBTC.Close = df1DayBTC.Close.map('{:.8f}'.format)

        df1Day = CalcEMA(df1Day,200,'EMA200',point)
        df1Day = CalcEMA(df1Day,100,'EMA100',point)
        df1Day = CalcEMA(df1Day,75,'EMA75',point)
        df1Day = CalcEMA(df1Day,50,'EMA50',point)
        df1Day = CalcEMA(df1Day,25,'EMA25',point)
        df1DayBTC = CalcEMABTC(df1DayBTC,200,'EMA200')
        df1DayBTC = CalcEMABTC(df1DayBTC,100,'EMA100')
        df1DayBTC = CalcEMABTC(df1DayBTC,75,'EMA75')
        df1DayBTC = CalcEMABTC(df1DayBTC,50,'EMA50')
        df1DayBTC = CalcEMABTC(df1DayBTC,25,'EMA25')

        # トレンドデータ
        TREND_PRICE = df1Day.Close.tail(30).astype(str).to_list()
        TREND_PRICE_BTC = df1DayBTC.Close.tail(30).astype(str).to_list()
        TREND_EMA200_1D = df1Day.EMA200.tail(30).astype(str).to_list()
        TREND_EMA100_1D = df1Day.EMA100.tail(30).astype(str).to_list()
        TREND_EMA75_1D = df1Day.EMA75.tail(30).astype(str).to_list()
        TREND_EMA50_1D = df1Day.EMA50.tail(30).astype(str).to_list()
        TREND_EMA25_1D = df1Day.EMA25.tail(30).astype(str).to_list()
        TREND_BTC_EMA200_1D = df1DayBTC.EMA200.tail(30).astype(str).to_list()
        TREND_BTC_EMA100_1D = df1DayBTC.EMA100.tail(30).astype(str).to_list()
        TREND_BTC_EMA75_1D = df1DayBTC.EMA75.tail(30).astype(str).to_list()
        TREND_BTC_EMA50_1D = df1DayBTC.EMA50.tail(30).astype(str).to_list()
        TREND_BTC_EMA25_1D = df1DayBTC.EMA25.tail(30).astype(str).to_list()

        getBTCPrice = lambda x: x[-1] if len(x) > 0 else 0

        d = {
            'pair':pair,
            'calcTime':now,
            'Price':lastPrice,
            'BTCPrice':lastPriceBTC,
            'EMA200_1D':TREND_EMA200_1D[-1],
            'EMA100_1D':TREND_EMA100_1D[-1],
            'EMA75_1D':TREND_EMA75_1D[-1],
            'EMA50_1D':TREND_EMA50_1D[-1],
            'EMA25_1D':TREND_EMA25_1D[-1],
            'BTC_EMA200_1D':getBTCPrice(TREND_BTC_EMA200_1D),
            'BTC_EMA100_1D':getBTCPrice(TREND_BTC_EMA100_1D),
            'BTC_EMA75_1D':getBTCPrice(TREND_BTC_EMA75_1D),
            'BTC_EMA50_1D':getBTCPrice(TREND_BTC_EMA50_1D),
            'BTC_EMA25_1D':getBTCPrice(TREND_BTC_EMA25_1D),
        }
        calcList.append(d)

        trend = {
            'pair':pair,
            'calcTime':now,
            'Price':{'VALUE':str(lastPrice),'TREND':TREND_PRICE},
            'PriceBTC':{'VALUE':str(lastPriceBTC),'TREND':TREND_PRICE_BTC},
            'EMA200_1D':{'VALUE':TREND_EMA200_1D[-1],'TREND':TREND_EMA200_1D},
            'EMA100_1D':{'VALUE':TREND_EMA100_1D[-1],'TREND':TREND_EMA100_1D},
            'EMA75_1D':{'VALUE':TREND_EMA75_1D[-1],'TREND':TREND_EMA75_1D},
            'EMA50_1D':{'VALUE':TREND_EMA50_1D[-1],'TREND':TREND_EMA50_1D},
            'EMA25_1D':{'VALUE':TREND_EMA25_1D[-1],'TREND':TREND_EMA25_1D},
            'BTC_EMA200_1D':{'VALUE':getBTCPrice(TREND_BTC_EMA200_1D),'TREND':TREND_BTC_EMA200_1D},
            'BTC_EMA100_1D':{'VALUE':getBTCPrice(TREND_BTC_EMA100_1D),'TREND':TREND_BTC_EMA100_1D},
            'BTC_EMA75_1D':{'VALUE':getBTCPrice(TREND_BTC_EMA75_1D),'TREND':TREND_BTC_EMA75_1D},
            'BTC_EMA50_1D':{'VALUE':getBTCPrice(TREND_BTC_EMA50_1D),'TREND':TREND_BTC_EMA50_1D},
            'BTC_EMA25_1D':{'VALUE':getBTCPrice(TREND_BTC_EMA25_1D),'TREND':TREND_BTC_EMA25_1D},
        }
        redisData.append(trend)

    return calcList,redisData

def TechnicalInfo2db(calcList,tablename):

    if not calcList:
        return
    
    query = 'INSERT INTO %s \
            (pair,calctime,price,BTCPrice, \
            EMA200_1D,EMA100_1D,EMA75_1D,EMA50_1D,EMA25_1D, \
            BTC_EMA200_1D,BTC_EMA100_1D,BTC_EMA75_1D,BTC_EMA50_1D,BTC_EMA25_1D \
            ) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

    for row in calcList:
        query1 = query % (
            tablename,
            row['pair'],
            row['calcTime'],
            row['Price'],
            row['BTCPrice'],
            row['EMA200_1D'],
            row['EMA100_1D'],
            row['EMA75_1D'],
            row['EMA50_1D'],
            row['EMA25_1D'],
            row['BTC_EMA200_1D'],
            row['BTC_EMA100_1D'],
            row['BTC_EMA75_1D'],
            row['BTC_EMA50_1D'],
            row['BTC_EMA25_1D'],
            )

        ENGINE.execute(query1)
    
def setRedis(redisData):
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'EMA_INFO'
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)
    setRedis2(client,key,redisData)

def setRedis2(client,key,redisData):

    for row in redisData:
        redisKey = key + '_' + row['pair']
        value = {
            'Pair':row['pair'],
            'Price':row['Price'],
            'EMA200':row['EMA200_1D'],
            'EMA100':row['EMA100_1D'],
            'EMA75':row['EMA75_1D'],
            'EMA50':row['EMA50_1D'],
            'EMA25':row['EMA25_1D'],
            'EMA200BTC':row['BTC_EMA200_1D'],
            'EMA100BTC':row['BTC_EMA100_1D'],
            'EMA75BTC':row['BTC_EMA75_1D'],
            'EMA50BTC':row['BTC_EMA50_1D'],
            'EMA25BTC':row['BTC_EMA25_1D'],
            'CalcTime':row['calcTime'],
        }
        jsonData= json.dumps(value,ensure_ascii=False)
        client.set(redisKey,jsonData)
        

if __name__ == "__main__":
    print('EMAデータ登録')
    main()
    calcList,redisData = main()
    setRedis(redisData)
    TechnicalInfo2db(calcList,'TECHNICAL_EMA')
