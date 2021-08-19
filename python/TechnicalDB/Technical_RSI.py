import pandas as pd
from const import *
from DBUtil2 import *
import datetime
import json
import redis

# RSIの計算
# データフレームに新規列(項目名:colName)を作成しspanで指定したRSIを入れる
# 引数で渡すデータフレームはローソク足データを想定
def CalcRSI(df,span,colName):
    
    # データフレームに入っている終値データで差分をとる
    # Forで回さなくても前回値との差分が取れるとか pandas最高
    diff = df.Close.diff()
    
    # 差分データをとりあえず upとdown (データフレーム型)として放り込む
    up,down = diff.copy(),diff.copy()
    
    # up は差分がマイナスの行は0 downは差分がプラスの行は0とする 
    up[up < 0] = 0
    down[down > 0] = 0

    # 指数平滑移動平均で計算する。downの方はマイナス値なので絶対値とってから計算
    upema = up.ewm(span-1).mean()
    downema = down.abs().ewm(span-1).mean()

    # RSI計算して新しい列に放り込む
    df[colName] = round(upema/(upema+downema)*100,2)

    # 小数点いらんやろ。。。多分。。。。
    df[colName] = df[colName].fillna(0)

    # デバッグ用
    #pd.set_option('display.max_rows', None)
    #print(df.loc[:,['openTime','close','RSI']])

    return df

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
 
        # Tickerデータとローソク足データを取得
        dfTicker = GetTickerData('BINANCE_TICKER_INFO',pair,80)
        dfTicker = dfTicker.rename(columns={'price':'Close'})
        df15Min = GetKlinesData('BINANCE_KLINES_15MIN',pair,80)
        df1Hour = GetKlinesData('BINANCE_KLINES_1HOUR',pair,80)
        df4Hour = GetKlinesData('BINANCE_KLINES_4HOUR',pair,80)
        df6Hour = GetKlinesData('BINANCE_KLINES_6HOUR',pair,80)
        df1Day = GetKlinesData('BINANCE_KLINES_1DAY',pair,80)

        #最終価格取得
        lastPrice = dfTicker.Close.iloc[-1]

        # ローソク足データの最終行の終値に現在価格を入れる
        df15Min.Close.iloc[-1] = lastPrice
        df1Hour.Close.iloc[-1] = lastPrice
        df4Hour.Close.iloc[-1] = lastPrice
        df6Hour.Close.iloc[-1] = lastPrice
        df1Day.Close.iloc[-1] = lastPrice

        # RSI計算
        dfTicker = CalcRSI(dfTicker,14,'RSI14')
        df15Min = CalcRSI(df15Min,14,'RSI14')
        df1Hour = CalcRSI(df1Hour,14,'RSI14')
        df4Hour = CalcRSI(df4Hour,14,'RSI14')
        df6Hour = CalcRSI(df6Hour,14,'RSI14')
        df1Day = CalcRSI(df1Day,14,'RSI14')

        # 瞬時値
        RSI14_1Min = dfTicker.RSI14.iloc[-1]
        RSI14_15Min = df15Min.RSI14.iloc[-1]
        RSI14_1Hour = df1Hour.RSI14.iloc[-1]
        RSI14_4Hour = df4Hour.RSI14.iloc[-1]
        RSI14_6Hour = df6Hour.RSI14.iloc[-1]
        RSI14_1Day = df1Day.RSI14.iloc[-1]

        # トレンドデータ
        TREND_PRICE = dfTicker.Close.tail(30).astype(str).to_list()
        TREND_1M = dfTicker.RSI14.tail(30).astype(str).to_list()
        TREND_15M = df15Min.RSI14.tail(30).astype(str).to_list()
        TREND_1H = df1Hour.RSI14.tail(30).astype(str).to_list()
        TREND_4H = df4Hour.RSI14.tail(30).astype(str).to_list()
        TREND_6H = df6Hour.RSI14.tail(30).astype(str).to_list()
        TREND_1D = df1Day.RSI14.tail(30).astype(str).to_list()


        d = {
            'pair':pair,
            'calcTime':now,
            'Price':lastPrice,
            'RSI14_1M':RSI14_1Min,
            'RSI14_15M':RSI14_15Min,
            'RSI14_1H':RSI14_1Hour,
            'RSI14_4H':RSI14_4Hour,
            'RSI14_6H':RSI14_6Hour,
            'RSI14_1D':RSI14_1Day,
        }
        calcList.append(d)

        trend = {
            'pair':pair,
            'calcTime':now,
            'Price':{'VALUE':str(lastPrice),'TREND':TREND_PRICE},
            'RSI14_1M':{'VALUE':str(RSI14_1Min),'TREND':TREND_1M},
            'RSI14_15M':{'VALUE':str(RSI14_15Min),'TREND':TREND_15M},
            'RSI14_1H':{'VALUE':str(RSI14_1Hour),'TREND':TREND_1H},
            'RSI14_4H':{'VALUE':str(RSI14_4Hour),'TREND':TREND_4H},
            'RSI14_6H':{'VALUE':str(RSI14_6Hour),'TREND':TREND_6H},
            'RSI14_1D':{'VALUE':str(RSI14_1Day),'TREND':TREND_1D},
        }
        redisData.append(trend)

    return calcList,redisData

def TechnicalInfo2db(calcList,tablename):

    if not calcList:
        return
    
    query = 'INSERT INTO %s \
            (pair,calctime,price,1min,15min,1hour,4hour,6hour,1day) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s,%s) '

    for row in calcList:
        query1 = query % (
            tablename,
            row['pair'],
            row['calcTime'],
            row['Price'],
            row['RSI14_1M'],
            row['RSI14_15M'],
            row['RSI14_1H'],
            row['RSI14_4H'],
            row['RSI14_6H'],
            row['RSI14_1D'],
            )

        ENGINE.execute(query1)
    
def setRedis(redisData):
    client = redis.Redis(host='localhost',port=26379,db=0)

    key = 'RSI_INFO'
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)
    setRedis2(client,key,redisData)

def setRedis2(client,key,redisData):

    for row in redisData:
        redisKey = key + '_' + row['pair']
        value = {
            'Pair':row['pair'],
            'Price':row['Price'],
            'RSI14_1M':row['RSI14_1M'],
            'RSI14_15M':row['RSI14_15M'],
            'RSI14_1H':row['RSI14_1H'],
            'RSI14_4H':row['RSI14_4H'],
            'RSI14_6H':row['RSI14_6H'],
            'RSI14_1D':row['RSI14_1D'],
            'CalcTime':row['calcTime'],
        }
        jsonData= json.dumps(value,ensure_ascii=False)
        client.set(redisKey,jsonData)
        

if __name__ == "__main__":
    print('RSIデータ登録')
    calcList,redisData = main()
    setRedis(redisData)
    TechnicalInfo2db(calcList,'TECHNICAL_RSI')

