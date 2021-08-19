import pandas as pd
from const import *
from DBUtil2 import *
import datetime
import json
import redis

# ボリンジャーバンド計算
def CalcBollingerBand(df,span,point):
    df['BBSMA'] = round(df.Close.rolling(window=span).mean(),point)
    df['STD'] = df.Close.rolling(window=span).std()
    #df['BBU1'] = round(df.BBSMA + (df.STD*1),point)
    df['BBU2'] = round(df.BBSMA + (df.STD*2),point)
    #df['BBU3'] = round(df.BBSMA + (df.STD*3),point)
    #df['BBL1'] = round(df.BBSMA - (df.STD*1),point)
    df['BBL2'] = round(df.BBSMA - (df.STD*2),point)
    #df['BBL3'] = round(df.BBSMA - (df.STD*3),point)
    # ボリンジャーバンド幅
    #df['BBW1'] = round(df.BBU1 - df.BBL1,point)
    df['BBW2'] = round(df.BBU2 - df.BBL2,point)
    #df['BBW3'] = round(df.BBU3 - df.BBL3,point)
    # ボリンジャーバンド幅率
    #df['BBWR1'] = round((df.BBU1/df.BBSMA*100-100)*2,2)
    df['BBWR2'] = round((df.BBU2/df.BBSMA*100-100)*2,2)
    #df['BBWR3'] = round((df.BBU3/df.BBSMA*100-100)*2,2)
    # 現在の水準
    #df['BBP1'] = df.Close - df.BBL1
    df['BBP2'] = df.Close - df.BBL2
    #df['BBP3'] = df.Close - df.BBL3
    # BB%B
    #df['BBB1'] = round(df.BBP1/df.BBW1,2)
    df['BBB2'] = round(df.BBP2/df.BBW2*100-50,2)
    #df['BBB3'] = round(df.BBP3/df.BBW3,2)
    df = df.fillna(0)
    return df

def dfBB2dict(df):

    d = {
        'SMA':df.BBSMA.iloc[-1],#SMA
        'UPR':df.BBU2.iloc[-1],#＋2σ
        'LWR':df.BBL2.iloc[-1],#ー2σ
        'BBB':df.BBB2.iloc[-1],#BB%B-50
        'BBWR':df.BBWR2.iloc[-1],#BB幅率
    }
    return d


def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # テクニカル演算のリストを作成
    calcList = []
    redisData = []
    redisData2 = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]
 
        # Tickerデータとローソク足データを取得
        dfTicker = GetTickerData('BINANCE_TICKER_INFO',pair,100)
        dfTicker = dfTicker.rename(columns={'price':'Close'})
        df15Min = GetKlinesData('BINANCE_KLINES_15MIN',pair,100)
        df1Hour = GetKlinesData('BINANCE_KLINES_1HOUR',pair,100)
        df4Hour = GetKlinesData('BINANCE_KLINES_4HOUR',pair,100)
        df1Day = GetKlinesData('BINANCE_KLINES_1DAY',pair,100)

        #最終価格取得
        lastPrice = dfTicker.Close.iloc[-1]

        # ローソク足データの最終行の終値に現在価格を入れる
        df15Min.Close.iloc[-1] = lastPrice
        df1Hour.Close.iloc[-1] = lastPrice
        df4Hour.Close.iloc[-1] = lastPrice
        df1Day.Close.iloc[-1] = lastPrice
        
        # BB
        #dfTicker = Technical2.CalcBollingerBandTicker(dfTicker,20,point)
        df15Min = CalcBollingerBand(df15Min,20,point)
        df1Hour = CalcBollingerBand(df1Hour,20,point)
        df4Hour = CalcBollingerBand(df4Hour,20,point)
        df1Day = CalcBollingerBand(df1Day,20,point)

        #BB_1Min = dfBB2dict(dfTicker,30)
        BB_15Min = dfBB2dict(df15Min)
        BB_1Hour = dfBB2dict(df1Hour)
        BB_4Hour = dfBB2dict(df4Hour)
        BB_1Day = dfBB2dict(df1Day)

        

        # トレンドデータ
        TREND_PRICE = dfTicker.Close.tail(30).astype(str).to_list()
        #TREND_1M = dfTicker.RSI14.tail(30).astype(str).to_list()
        TREND_SMA_15M = df15Min.BBSMA.tail(30).astype(str).to_list()
        TREND_BBU_15M = df15Min.BBU2.tail(30).astype(str).to_list()
        TREND_BBL_15M = df15Min.BBL2.tail(30).astype(str).to_list()
        TREND_BBWR_15M = df15Min.BBWR2.tail(30).astype(str).to_list()
        TREND_BBB_15M = df15Min.BBB2.tail(30).astype(str).to_list()
        
        TREND_SMA_1H = df1Hour.BBSMA.tail(30).astype(str).to_list()
        TREND_BBU_1H = df1Hour.BBU2.tail(30).astype(str).to_list()
        TREND_BBL_1H = df1Hour.BBL2.tail(30).astype(str).to_list()
        TREND_BBWR_1H = df1Hour.BBWR2.tail(30).astype(str).to_list()
        TREND_BBB_1H = df1Hour.BBB2.tail(30).astype(str).to_list()
        
        TREND_SMA_4H = df4Hour.BBSMA.tail(30).astype(str).to_list()
        TREND_BBU_4H = df4Hour.BBU2.tail(30).astype(str).to_list()
        TREND_BBL_4H = df4Hour.BBL2.tail(30).astype(str).to_list()
        TREND_BBWR_4H = df4Hour.BBWR2.tail(30).astype(str).to_list()
        TREND_BBB_4H = df4Hour.BBB2.tail(30).astype(str).to_list()
        
        TREND_SMA_1D = df1Day.BBSMA.tail(30).astype(str).to_list()
        TREND_BBU_1D = df1Day.BBU2.tail(30).astype(str).to_list()
        TREND_BBL_1D = df1Day.BBL2.tail(30).astype(str).to_list()
        TREND_BBWR_1D = df1Day.BBWR2.tail(30).astype(str).to_list()
        TREND_BBB_1D = df1Day.BBB2.tail(30).astype(str).to_list()

        d = {
            'pair':pair,
            'calcTime':now,
            'Price':lastPrice,
            'SMA_15M':BB_15Min['SMA'],
            'UPR_15M':BB_15Min['UPR'],
            'LWR_15M':BB_15Min['LWR'],
            'BBB_15M':BB_15Min['BBB'],
            'BBWR_15M':BB_15Min['BBWR'],
            'SMA_1H':BB_1Hour['SMA'],
            'UPR_1H':BB_1Hour['UPR'],
            'LWR_1H':BB_1Hour['LWR'],
            'BBB_1H':BB_1Hour['BBB'],
            'BBWR_1H':BB_1Hour['BBWR'],
            'SMA_4H':BB_4Hour['SMA'],
            'UPR_4H':BB_4Hour['UPR'],
            'LWR_4H':BB_4Hour['LWR'],
            'BBB_4H':BB_4Hour['BBB'],
            'BBWR_4H':BB_4Hour['BBWR'],
            'SMA_1D':BB_1Day['SMA'],
            'UPR_1D':BB_1Day['UPR'],
            'LWR_1D':BB_1Day['LWR'],
            'BBB_1D':BB_1Day['BBB'],
            'BBWR_1D':BB_1Day['BBWR'],
        }
        calcList.append(d)
        '''
        trend = {
            'pair':pair,
            'calcTime':now,
            'Price':{'VALUE':str(lastPrice),'TREND':TREND_PRICE},
            'SMA_15M':{'VALUE':str(TREND_SMA_15M[-1]),'TREND':TREND_SMA_15M},
            'BBU_15M':{'VALUE':str(TREND_BBU_15M[-1]),'TREND':TREND_BBU_15M},
            'BBL_15M':{'VALUE':str(TREND_BBL_15M[-1]),'TREND':TREND_BBL_15M},
            'BBB_15M':{'VALUE':str(TREND_BBB_15M[-1]),'TREND':TREND_BBB_15M},
            'BBWR_15M':{'VALUE':str(TREND_BBWR_15M[-1]),'TREND':TREND_BBWR_15M},
            'SMA_1H':{'VALUE':str(TREND_SMA_1H[-1]),'TREND':TREND_SMA_1H},
            'BBU_1H':{'VALUE':str(TREND_BBU_1H[-1]),'TREND':TREND_BBU_1H},
            'BBL_1H':{'VALUE':str(TREND_BBL_1H[-1]),'TREND':TREND_BBL_1H},
            'BBB_1H':{'VALUE':str(TREND_BBB_1H[-1]),'TREND':TREND_BBB_1H},
            'BBWR_1H':{'VALUE':str(TREND_BBWR_1H[-1]),'TREND':TREND_BBWR_1H},
            'SMA_4H':{'VALUE':str(TREND_SMA_4H[-1]),'TREND':TREND_SMA_4H},
            'BBU_4H':{'VALUE':str(TREND_BBU_4H[-1]),'TREND':TREND_BBU_4H},
            'BBL_4H':{'VALUE':str(TREND_BBL_4H[-1]),'TREND':TREND_BBL_4H},
            'BBB_4H':{'VALUE':str(TREND_BBB_4H[-1]),'TREND':TREND_BBB_4H},
            'BBWR_4H':{'VALUE':str(TREND_BBWR_4H[-1]),'TREND':TREND_BBWR_4H},
            'SMA_1D':{'VALUE':str(TREND_SMA_1D[-1]),'TREND':TREND_SMA_1D},
            'BBU_1D':{'VALUE':str(TREND_BBU_1D[-1]),'TREND':TREND_BBU_1D},
            'BBL_1D':{'VALUE':str(TREND_BBL_1D[-1]),'TREND':TREND_BBL_1D},
            'BBB_1D':{'VALUE':str(TREND_BBB_1D[-1]),'TREND':TREND_BBB_1D},
            'BBWR_1D':{'VALUE':str(TREND_BBWR_1D[-1]),'TREND':TREND_BBWR_1D},
        }
        '''
        trend = {
            'pair':pair,
            'calcTime':now,
            'Price':{'VALUE':str(lastPrice),'TREND':TREND_PRICE},
            'BBB_15M':{'VALUE':str(TREND_BBB_15M[-1]),'TREND':TREND_BBB_15M},
            'BBB_1H':{'VALUE':str(TREND_BBB_1H[-1]),'TREND':TREND_BBB_1H},
            'BBB_4H':{'VALUE':str(TREND_BBB_4H[-1]),'TREND':TREND_BBB_4H},
            'BBB_1D':{'VALUE':str(TREND_BBB_1D[-1]),'TREND':TREND_BBB_1D},
        }
        trend2 = {
            'pair':pair,
            'calcTime':now,
            'Price':{'VALUE':str(lastPrice),'TREND':TREND_PRICE},
            'BBWR_15M':{'VALUE':str(TREND_BBWR_15M[-1]),'TREND':TREND_BBWR_15M},
            'BBWR_1H':{'VALUE':str(TREND_BBWR_1H[-1]),'TREND':TREND_BBWR_1H},
            'BBWR_4H':{'VALUE':str(TREND_BBWR_4H[-1]),'TREND':TREND_BBWR_4H},
            'BBWR_1D':{'VALUE':str(TREND_BBWR_1D[-1]),'TREND':TREND_BBWR_1D},
        }
        redisData.append(trend)
        redisData2.append(trend2)

    return calcList,redisData,redisData2

def TechnicalInfo2db(calcList,tablename):

    if not calcList:
        return
    
    query = 'INSERT INTO %s \
            (pair,calctime,price, \
            SMA_15M,UPR_15M,LWR_15M,BBB_15M,BBWR_15M, \
            SMA_1H,UPR_1H,LWR_1H,BBB_1H,BBWR_1H, \
            SMA_4H,UPR_4H,LWR_4H,BBB_4H,BBWR_4H, \
            SMA_1D,UPR_1D,LWR_1D,BBB_1D,BBWR_1D \
            ) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

    for row in calcList:
        query1 = query % (
            tablename,
            row['pair'],
            row['calcTime'],
            row['Price'],
            row['SMA_15M'],
            row['UPR_15M'],
            row['LWR_15M'],
            row['BBB_15M'],
            row['BBWR_15M'],
            row['SMA_1H'],
            row['UPR_1H'],
            row['LWR_1H'],
            row['BBB_1H'],
            row['BBWR_1H'],
            row['SMA_4H'],
            row['UPR_4H'],
            row['LWR_4H'],
            row['BBB_4H'],
            row['BBWR_4H'],
            row['SMA_1D'],
            row['UPR_1D'],
            row['LWR_1D'],
            row['BBB_1D'],
            row['BBWR_1D'],
            )

        ENGINE.execute(query1)
    
def setRedis(redisData):
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'BB_INFO'
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)

def setRedis2(redisData):
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'BB_INFO2'
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)


if __name__ == "__main__":
    print('BBデータ登録')
    calcList,redisData,redisData2 = main()
    setRedis(redisData)
    setRedis2(redisData2)
    #print(calcList)
    TechnicalInfo2db(calcList,'TECHNICAL_BB')

