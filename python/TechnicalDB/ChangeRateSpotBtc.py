
from setting import session
from BinanceTableModel import *
from const import *
import pandas as pd
import datetime
import redis
import json

def GetChangeRate(tablename):

    #定義
    PRICE_001MIN_AGO = 'Price001minAgo'
    PRICE_005MIN_AGO = 'Price005minAgo'
    PRICE_010MIN_AGO = 'Price010minAgo'
    PRICE_030MIN_AGO = 'Price030minAgo'
    PRICE_060MIN_AGO = 'Price060minAgo'
    #PRICE_120MIN_AGO = 'Price120minAgo'
    PRICE_240MIN_AGO = 'Price240minAgo'
    PRICE_360MIN_AGO = 'Price360minAgo'
    PRICE_480MIN_AGO = 'Price480minAgo'
    PRICE_720MIN_AGO = 'Price720minAgo'

    CHANGE_RATE_001 = 'ChangeRate1'
    CHANGE_RATE_005 = 'ChangeRate5'
    CHANGE_RATE_010 = 'ChangeRate10'
    CHANGE_RATE_030 = 'ChangeRate30'
    CHANGE_RATE_060 = 'ChangeRate60'
    #CHANGE_RATE_120 = 'ChangeRate120'
    CHANGE_RATE_240 = 'ChangeRate240'
    CHANGE_RATE_360 = 'ChangeRate360'
    CHANGE_RATE_480 = 'ChangeRate480'
    CHANGE_RATE_720 = 'ChangeRate720'


    print("変動率を計算します")
    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER_SPOT_BTC.symbol,BINANCE_SYMBOL_MASTER_SPOT_BTC.point)

    # 変動率のリストを作成
    changeRateList = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        point = symbol[1]

        query = 'select * from %s where symbol = "%s" order by tickerTime desc limit 721'
        query1 = query % (tablename,pair)
        df = pd.read_sql_query(con=ENGINE,sql=query1)
        df[PRICE_001MIN_AGO] = df[PRICE_].shift(-1)
        df[PRICE_005MIN_AGO] = df[PRICE_].shift(-5)
        df[PRICE_010MIN_AGO] = df[PRICE_].shift(-10)
        df[PRICE_030MIN_AGO] = df[PRICE_].shift(-30)
        df[PRICE_060MIN_AGO] = df[PRICE_].shift(-60)
        #df[PRICE_120MIN_AGO] = df[PRICE_].shift(-120)
        df[PRICE_240MIN_AGO] = df[PRICE_].shift(-240)
        df[PRICE_360MIN_AGO] = df[PRICE_].shift(-360)
        df[PRICE_480MIN_AGO] = df[PRICE_].shift(-480)
        df[PRICE_720MIN_AGO] = df[PRICE_].shift(-720)

        df[CHANGE_RATE_001] = df[PRICE_]/df[PRICE_001MIN_AGO]*100-100
        df[CHANGE_RATE_005] = df[PRICE_]/df[PRICE_005MIN_AGO]*100-100
        df[CHANGE_RATE_010] = df[PRICE_]/df[PRICE_010MIN_AGO]*100-100
        df[CHANGE_RATE_030] = df[PRICE_]/df[PRICE_030MIN_AGO]*100-100
        df[CHANGE_RATE_060] = df[PRICE_]/df[PRICE_060MIN_AGO]*100-100
        #df[CHANGE_RATE_120] = df[PRICE_]/df[PRICE_120MIN_AGO]*100-100
        df[CHANGE_RATE_240] = df[PRICE_]/df[PRICE_240MIN_AGO]*100-100
        df[CHANGE_RATE_360] = df[PRICE_]/df[PRICE_360MIN_AGO]*100-100
        df[CHANGE_RATE_480] = df[PRICE_]/df[PRICE_480MIN_AGO]*100-100
        df[CHANGE_RATE_720] = df[PRICE_]/df[PRICE_720MIN_AGO]*100-100

        df[TICKER_TIME_] = df[TICKER_TIME_].astype(str)
        df = df.fillna(0)

        df[PRICE_] = df.price.map('{:.8f}'.format)

        TREND_PRICE = df.price.tail(30).to_list()

        data = {
            "pair":pair,
            "point":point,
            "price":{'VALUE':df.iloc[0][PRICE_],'TREND':TREND_PRICE},
            "CRate01":str(round(df.iloc[0][CHANGE_RATE_001],2)),
            "CRate05": str(round(df.iloc[0][CHANGE_RATE_005],2)),
            "CRate10":str(round(df.iloc[0][CHANGE_RATE_010],2)),
            "CRate30":str(round(df.iloc[0][CHANGE_RATE_030],2)),
            "CRate60":str(round(df.iloc[0][CHANGE_RATE_060],2)),
            #"CRate120":str(round(df.iloc[0][CHANGE_RATE_120],2)),
            "CRate240":str(round(df.iloc[0][CHANGE_RATE_240],2)),
            "CRate360":str(round(df.iloc[0][CHANGE_RATE_360],2)),
            "CRate480":str(round(df.iloc[0][CHANGE_RATE_480],2)),
            "CRate720":str(round(df.iloc[0][CHANGE_RATE_720],2)),
            'calcTime':df.iloc[0][TICKER_TIME_],
        }
        if data['CRate05']=="0.0" and data['CRate10']=="0.0" and data['CRate30']=="0.0" and data['CRate60']=="0.0" and data['CRate240']=="0.0":
            pass
        else:
            changeRateList.append(data)

    return json.dumps(changeRateList,ensure_ascii=False)



def main():
    #本番環境
    #client = redis.Redis(host='localhost',port=26379,db=0)
    #DEBUG環境
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'ChangeRateSpotBtc'
    value = GetChangeRate('BINANCE_TICKER_INFO_SPOT_BTC')
    #print(value)
    client.set(key,value)

if __name__ == "__main__":
    main()