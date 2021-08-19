import json
import redis
from setting import session
from DBUtil3 import *

def df2dict(df1M,df15M,df1H,df4H,df6H,df1D,calcTime):
    d = {
        'Pair':df1M.symbol.iloc[-1],
        'Value':df1M.Close.iloc[-1].astype(str),
        'Trend':{
            '1M':df1M.Close.astype(str).to_list(),
            '15M':df15M.Close.astype(str).to_list(),
            '1H':df1H.Close.astype(str).to_list(),
            '4H':df4H.Close.astype(str).to_list(),
            '6H':df6H.Close.astype(str).to_list(),
            '1D':df1D.Close.astype(str).to_list(),
        },
        'CalcTime':calcTime,
    }

    return d

def setRedis(client,pair,redisData):
    info = 'Price'
    key = 'Trend_' + info + '_' + pair
    value = json.dumps(redisData,ensure_ascii=False)
    client.set(key,value)

def main():

    client = redis.Redis(host='redis',port=6379,db=0)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # シンボルリストをDBから取得
    symbolList = GetSymbolList()

    # テクニカル演算のリストを作成
    calcList = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]

        # トレンドデータ取得
        df1M = GetTickerData('BINANCE_TICKER_INFO',pair,30) # 30分
        df1M = df1M.rename(columns={'price':'Close'})
        df15M = GetKlinesCloseData('BINANCE_KLINES_15MIN',pair,30)  # 7.5時間
        df1H = GetKlinesCloseData('BINANCE_KLINES_1HOUR',pair,30)   # 30時間
        df4H = GetKlinesCloseData('BINANCE_KLINES_4HOUR',pair,30)   # 120時間
        df6H = GetKlinesCloseData('BINANCE_KLINES_6HOUR',pair,30)   # 180時間
        df1D = GetKlinesCloseData('BINANCE_KLINES_1DAY',pair,30)    # 30日

        # 現在価格
        lastPrice = df1M.Close.iloc[-1]

        # ローソク足データは取得間隔が長いのでTickerデータを最終値にいれる
        df15M.Close.iloc[-1] = lastPrice
        df1H.Close.iloc[-1] = lastPrice
        df4H.Close.iloc[-1] = lastPrice
        df6H.Close.iloc[-1] = lastPrice
        df1D.Close.iloc[-1] = lastPrice

        #print(df1M,df15M,df1H,df4H,df1D)
        d = df2dict(df1M,df15M,df1H,df4H,df6H,df1D,now)
        setRedis(client,pair,d)

if __name__ == "__main__":
    print('各銘柄のSparkLine用トレンドデータをredisに登録します。')
    main()
