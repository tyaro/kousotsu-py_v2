import pandas as pd
from const import *
from DBUtil2 import *
import datetime
from Technical import *
import json
import redis

# テクニカル分析用クラス
class Technical2:

    # RSIの計算
    # データフレームに新規列(項目名:colName)を作成しspanで指定したRSIを入れる
    # 引数で渡すデータフレームはローソク足データを想定
    @staticmethod
    def CalcRSI(df,span,colName):
        
        # データフレームに入っている終値データで差分をとる
        # Forで回さなくても前回値との差分が取れるとか pandas最高
        diff = df.price.diff()
        
        # 差分データをとりあえず upとdown (データフレーム型)として放り込む
        up,down = diff.copy(),diff.copy()
        
        # up は差分がマイナスの行は0 downは差分がプラスの行は0とする 
        up[up < 0] = 0
        down[down > 0] = 0

        # 指数平滑移動平均で計算する。downの方はマイナス値なので絶対値とってから計算
        upema = up.ewm(span-1).mean()
        downema = down.abs().ewm(span-1).mean()

        # RSI計算して新しい列に放り込む
        df[colName] = upema/(upema+downema)*100

        # 小数点いらんやろ。。。多分。。。。
        df[colName] = df[colName].fillna(0).astype('int')

        # デバッグ用
        #pd.set_option('display.max_rows', None)
        #print(df.loc[:,['openTime','close','RSI']])

        return df

    @staticmethod
    def CalcARR(df,span1,span2,span3,colName1,colName2,colName3):
        df['VRate'] = round((df.High/df.Close*100-100).abs() + (df.Low/df.Close*100-100).abs(),2)
        df[colName1] = round(df.VRate.rolling(span1,center=False).mean(),2)
        df[colName2] = round(df.VRate.rolling(span2,center=False).mean(),2)
        df[colName3] = round(df.VRate.rolling(span3,center=False).mean(),2)

        return df

    @staticmethod
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
        df['BBB2'] = round(df.BBP2/df.BBW2,2)
        #df['BBB3'] = round(df.BBP3/df.BBW3,2)
        return df

    @staticmethod
    def CalcBollingerBandTicker(df,span,point):
        df['BBSMA'] = round(df.price.rolling(window=span).mean().fillna(0),point)
        df['STD'] = df.price.rolling(window=span).std().fillna(0)

        df['BBU1'] = round(df.BBSMA + (df.STD*1),point)
        df['BBU2'] = round(df.BBSMA + (df.STD*2),point)
        df['BBU3'] = round(df.BBSMA + (df.STD*3),point)
        df['BBL1'] = round(df.BBSMA - (df.STD*1),point)
        df['BBL2'] = round(df.BBSMA - (df.STD*2),point)
        df['BBL3'] = round(df.BBSMA - (df.STD*3),point)
        # ボリンジャーバンド幅
        df['BBW1'] = round(df.BBU1 - df.BBL1,point)
        df['BBW2'] = round(df.BBU2 - df.BBL2,point)
        df['BBW3'] = round(df.BBU3 - df.BBL3,point)
        # ボリンジャーバンド幅率
        df['BBWR1'] = round((df.BBU1/df.BBSMA*100-100)*2,2)
        df['BBWR2'] = round((df.BBU2/df.BBSMA*100-100)*2,2)
        df['BBWR3'] = round((df.BBU3/df.BBSMA*100-100)*2,2)
        # 現在の水準
        df['BBP1'] = df.price - df.BBL1
        df['BBP2'] = df.price - df.BBL2
        df['BBP3'] = df.price - df.BBL3
        # BB%B
        df['BBB1'] = round(df.BBP1/df.BBW1,2)
        df['BBB2'] = round(df.BBP2/df.BBW2,2)
        df['BBB3'] = round(df.BBP3/df.BBW3,2)
        return df

    # BTCとの連動率を計算(24時間分) EMA使用
    # BTCデータフレームには既にUpRate DownRateの計算結果が入っているものとする
    @staticmethod
    def GetFriendRate(df,dfBTC):
        df = Technical.CalcUpDownRate(df,24,UP_RATE_,DOWN_RATE_)
        dfBTC = Technical.CalcUpDownRate(dfBTC,24,UP_RATE_,DOWN_RATE_)
        df = Technical.CalcBTCFriendRate(dfBTC,df,UP_RATE_,DOWN_RATE_,FRIEND_RATE_UP_,FRIEND_RATE_DOWN_)
        return df

    # 乖離率計算
    # base:基準
    # value:評価対象
    @staticmethod
    def DeviationRate(base,value):
        if base == 0.0:
            return 0.0
        value = round((value/base) * 100 - 100,1)
        return value

def dfBB2dict(df,span):
    BBWR = df.BBWR2.tail(span).astype(str).to_list()
    #BBB1 = df.BBB1.tail(span).astype(str).to_list()
    BBB2 = df.BBB2.tail(span).astype(str).to_list()
    #BBB3 = df.BBB3.tail(span).astype(str).to_list()

    d = {
        'SMA':str(df.BBSMA.iloc[-1]),
        'BB2':{
            'UPPER':str(df.BBU2.iloc[-1]),
            'LOWER':str(df.BBL2.iloc[-1]),
            'BBB':BBB2,
        },
        'BBWR':BBWR,
    }
    return d

def dfARR2dict(df):
    d ={
        'ARR0':str(df.VRate.iloc[-1]),
        'ARR5':str(df.ARR5.iloc[-1]),
        'ARR10':str(df.ARR10.iloc[-1]),
        'ARR20':str(df.ARR20.iloc[-1]),
    }
    return d

def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # テクニカル演算のリストを作成
    calcList = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]
 
        # Tickerデータとローソク足データを取得
        dfTicker = GetTickerData('BINANCE_TICKER_INFO',pair,80)
        df15Min = GetKlinesData('BINANCE_KLINES_15MIN',pair,80)
        df1Hour = GetKlinesData('BINANCE_KLINES_1HOUR',pair,80)
        df4Hour = GetKlinesData('BINANCE_KLINES_4HOUR',pair,80)
        df1Day = GetKlinesData('BINANCE_KLINES_1DAY',pair,50)

        #最終価格取得
        lastPrice = dfTicker.price.iloc[-1]

        # ローソク足データの最終行の終値に現在価格を入れる
        df15Min.Close.iloc[-1] = lastPrice
        df1Hour.Close.iloc[-1] = lastPrice
        df4Hour.Close.iloc[-1] = lastPrice

        # RSI計算
        dfTicker = Technical2.CalcRSI(dfTicker,14,'RSI14')
        df15Min = Technical.CalcRSI(df15Min,14,'RSI14')
        df1Hour = Technical.CalcRSI(df1Hour,14,'RSI14')
        df4Hour = Technical.CalcRSI(df4Hour,14,'RSI14')
        df1Day = Technical.CalcRSI(df1Day,14,'RSI14')

        # ARR
        #df15Min = Technical2.CalcARR(df15Min,5,10,20,'ARR5','ARR10','ARR20')
        #df1Hour = Technical2.CalcARR(df1Hour,5,10,20,'ARR5','ARR10','ARR20')
        #df4Hour = Technical2.CalcARR(df4Hour,5,10,20,'ARR5','ARR10','ARR20')
        df1Day = Technical2.CalcARR(df1Day,5,10,20,'ARR5','ARR10','ARR20')

        # BB
        #dfTicker = Technical2.CalcBollingerBandTicker(dfTicker,20,point)
        df15Min = Technical2.CalcBollingerBand(df15Min,20,point)
        df1Hour = Technical2.CalcBollingerBand(df1Hour,20,point)
        df4Hour = Technical2.CalcBollingerBand(df4Hour,20,point)
        df1Day = Technical2.CalcBollingerBand(df1Day,20,point)

        # list1加工
        price = dfTicker.price.tail(30).astype(str).to_list()

        RSI14_1Min = dfTicker.RSI14.tail(30).astype(str).to_list()
        RSI14_15Min = df15Min.RSI14.tail(30).astype(str).to_list()
        RSI14_1Hour = df1Hour.RSI14.tail(30).astype(str).to_list()
        RSI14_4Hour = df4Hour.RSI14.tail(30).astype(str).to_list()
        RSI14_1Day = df1Day.RSI14.tail(30).astype(str).to_list()

        #BB_1Min = dfBB2dict(dfTicker,30)
        BB_15Min = dfBB2dict(df15Min,30)
        BB_1Hour = dfBB2dict(df1Hour,30)
        BB_4Hour = dfBB2dict(df4Hour,30)
        BB_1Day = dfBB2dict(df1Day,30)

        # dict加工
        #ARR_15Min = dfARR2dict(df15Min)
        #ARR_1Hour = dfARR2dict(df1Hour)
        #ARR_4Hour = dfARR2dict(df4Hour)
        ARR_1Day = dfARR2dict(df1Day)

        d = {
            'pair':pair,
            'Price':price,
            'RSI14_1M':RSI14_1Min,
            'RSI14_15M':RSI14_15Min,
            'RSI14_1H':RSI14_1Hour,
            'RSI14_4H':RSI14_4Hour,
            'RSI14_1D':RSI14_1Day,
            #'ARR_15M':ARR_15Min,
            #'ARR_1H':ARR_1Hour,
            #'ARR_4H':ARR_4Hour,
            'ARR_1D':ARR_1Day,
            #'BB_1M':BB_1Min,
            'BB_15M':BB_15Min,
            'BB_1H':BB_1Hour,
            'BB_4H':BB_4Hour,
            'BB_1D':BB_1Day,
        }

        calcList.append(d)

    return calcList




if __name__ == "__main__":
    calcList = main()

    client = redis.Redis(host='localhost',port=26379,db=0)

    key = 'Technical2'
    value = json.dumps(calcList,ensure_ascii=False)
    client.set(key,value)


