
from setting import session
from BinanceTableModel import *
from const import *
import pandas as pd
import datetime
import redis
import json

def GetChangeRate(tablename):

    #定義
    PRICE_005MIN_AGO = 'Price005minAgo'
    PRICE_010MIN_AGO = 'Price010minAgo'
    PRICE_030MIN_AGO = 'Price030minAgo'
    PRICE_060MIN_AGO = 'Price060minAgo'
    PRICE_120MIN_AGO = 'Price120minAgo'

    CHANGE_RATE_005 = 'ChangeRate5'
    CHANGE_RATE_010 = 'ChangeRate10'
    CHANGE_RATE_030 = 'ChangeRate30'
    CHANGE_RATE_060 = 'ChangeRate60'
    CHANGE_RATE_120 = 'ChangeRate120'


    print("変動率を計算します")
    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # 変動率のリストを作成
    changeRateList = []
    # 全銘柄(5分/10分/30分/120分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        point = symbol[1]

        query = 'select * from %s where symbol = "%s" order by tickerTime desc limit 120'
        query1 = query % (tablename,pair)
        df = pd.read_sql_query(con=ENGINE,sql=query1)
        df[PRICE_005MIN_AGO] = df[PRICE_].shift(-5)
        df[PRICE_010MIN_AGO] = df[PRICE_].shift(-10)
        df[PRICE_030MIN_AGO] = df[PRICE_].shift(-30)
        df[PRICE_060MIN_AGO] = df[PRICE_].shift(-60)
        df[PRICE_120MIN_AGO] = df[PRICE_].shift(-120)

        df[CHANGE_RATE_005] = df[PRICE_]/df[PRICE_005MIN_AGO]*100-100
        df[CHANGE_RATE_010] = df[PRICE_]/df[PRICE_010MIN_AGO]*100-100
        df[CHANGE_RATE_030] = df[PRICE_]/df[PRICE_030MIN_AGO]*100-100
        df[CHANGE_RATE_060] = df[PRICE_]/df[PRICE_060MIN_AGO]*100-100
        df[CHANGE_RATE_120] = df[PRICE_]/df[PRICE_120MIN_AGO]*100-100

        df[TICKER_TIME_] = df[TICKER_TIME_].astype(str)

        data = {
                "pair": pair,
                "5min": round(df.iloc[0][CHANGE_RATE_005],2),
                "10min":round(df.iloc[0][CHANGE_RATE_010],2),
                "30min":round(df.iloc[0][CHANGE_RATE_030],2),
                "60min":round(df.iloc[0][CHANGE_RATE_060],2),
                "120min":round(df.iloc[0][CHANGE_RATE_120],2),
                'calcTime':df.iloc[0][TICKER_TIME_],
        }
        changeRateList.append(data)

    return json.dumps(changeRateList)



def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'ChangeRate'
    value = GetChangeRate('BINANCE_TICKER_INFO')
    #client.set('hoge','piyo')
    client.set(key,value)

if __name__ == "__main__":
    main()