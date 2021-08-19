import pandas as pd
from const import *
from DBUtil2 import *
import datetime
import json
import redis



def CalcARR(df,span1,span2,span3,colName1,colName2,colName3):
    df['VRate'] = round((df.High/df.Open*100-100).abs() + (df.Low/df.Open*100-100).abs(),2)
    df[colName1] = round(df.VRate.rolling(span1,center=False).mean(),2)
    df[colName2] = round(df.VRate.rolling(span2,center=False).mean(),2)
    df[colName3] = round(df.VRate.rolling(span3,center=False).mean(),2)

    return df

def CalcARRE(df,span1,span2,span3,colName1,colName2,colName3):
    df[colName1] = round(df.VRate.ewm(span1).mean(),2)
    df[colName2] = round(df.VRate.ewm(span2).mean(),2)
    df[colName3] = round(df.VRate.ewm(span3).mean(),2)

    return df

def dfARR2dict(df):
    d ={
        'ARR0':df.VRate.iloc[-1],
        'ARR5':df.ARR5.iloc[-2],
        'ARR10':df.ARR10.iloc[-2],
        'ARR20':df.ARR20.iloc[-2],
        'ARRE5':df.ARRE5.iloc[-2],
        'ARRE10':df.ARRE10.iloc[-2],
        'ARRE20':df.ARRE20.iloc[-2],
    }
    return d


def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # テクニカル演算のリストを作成
    calcList = []
    redisData = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]
 
        # ローソク足データを取得
        #dfTicker = GetTickerData('BINANCE_TICKER_INFO',pair,5)
        #dfTicker = dfTicker.rename(columns={'price':'Close'})
        df1Day = GetKlinesData('BINANCE_KLINES_1DAY',pair,50)
        df1H = GetKlinesData('BINANCE_KLINES_1HOUR',pair,5)
        #最終価格取得
        #lastPrice = dfTicker.Close.iloc[-1]
        lastPrice = df1H.Close.iloc[-1]

        # ローソク足データの最終行の終値に現在価格を入れる
        df1Day.Close.iloc[-1] = lastPrice
        if df1Day.High.iloc[-1] < lastPrice:
            df1Day.High.iloc[-1] = lastPrice
        if df1Day.Low.iloc[-1] > lastPrice:
            df1Day.Low.iloc[-1] = lastPrice

        # ARR
        df1Day = CalcARR(df1Day,5,10,20,'ARR5','ARR10','ARR20')
        df1Day = CalcARRE(df1Day,5,10,20,'ARRE5','ARRE10','ARRE20')

        ARR_1Day = dfARR2dict(df1Day)

        d = {
            'pair':pair,
            'calcTime':now,
            'Price':lastPrice,
            'ARR0':ARR_1Day['ARR0'],
            'ARR5':ARR_1Day['ARR5'],
            'ARR10':ARR_1Day['ARR10'],
            'ARR20':ARR_1Day['ARR20'],
            'ARRE5':ARR_1Day['ARRE5'],
            'ARRE10':ARR_1Day['ARRE10'],
            'ARRE20':ARR_1Day['ARRE20'],
        }
        trend = {
            'pair':pair,
            'calcTime':now,
            'Price':str(lastPrice),
            'ARR0':str(ARR_1Day['ARR0']),
            'ARR5':str(ARR_1Day['ARR5']),
            'ARR10':str(ARR_1Day['ARR10']),
            'ARR20':str(ARR_1Day['ARR20']),
            'ARRE5':str(ARR_1Day['ARRE5']),
            'ARRE10':str(ARR_1Day['ARRE10']),
            'ARRE20':str(ARR_1Day['ARRE20']),
        }
        calcList.append(d)
        redisData.append(trend)

    return calcList,redisData

def TechnicalInfo2db(calcList,tablename):

    if not calcList:
        return
    
    query = 'INSERT INTO %s \
            (pair,calctime,price,ATR,ARR5,ARR10,ARR20,ARRE5,ARRE10,ARRE20) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s,%s,%s) '

    for row in calcList:
        query1 = query % (
            tablename,
            row['pair'],
            row['calcTime'],
            row['Price'],
            row['ARR0'],
            row['ARR5'],
            row['ARR10'],
            row['ARR20'],
            row['ARRE5'],
            row['ARRE10'],
            row['ARRE20'],
            )

        ENGINE.execute(query1)
    
def setRedis(redisData):
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'ARR_INFO'
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)

if __name__ == "__main__":
    print('ARRデータ登録')
    calcList,redisData = main()
    setRedis(redisData)
    TechnicalInfo2db(calcList,'TECHNICAL_ARR')

