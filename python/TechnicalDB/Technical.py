import pandas as pd
from const import *
from DBUtil2 import *
import datetime

# テクニカル分析用クラス
class Technical:

    # RSIの計算
    # データフレームに新規列(項目名:colName)を作成しspanで指定したRSIを入れる
    # 引数で渡すデータフレームはローソク足データを想定
    @staticmethod
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
        df[colName] = upema/(upema+downema)*100

        # 小数点いらんやろ。。。多分。。。。
        df[colName] = df[colName].fillna(0).astype('int')

        # デバッグ用
        #pd.set_option('display.max_rows', None)
        #print(df.loc[:,['openTime','close','RSI']])

        return df

    # 上昇率/下落率の計算
    @staticmethod
    def CalcUpDownRate(df,span,colNameUp,colNameDown):
        # データフレームに入っている終値データで差分をとる
        # Forで回さなくても前回値との差分が取れるとか pandas最高
        diff = df[CLOSE_].diff()
        
        # 差分データをとりあえず upとdown (データフレーム型)として放り込む
        up,down = diff.copy(),diff.copy()
        
        # up は差分がマイナスの行は0 downは差分がプラスの行は0とする 
        up[up < 0] = 0
        down[down > 0] = 0

        # 指数平滑移動平均でUPEMAとDOWNEMAを計算する。(単位時間当たりのUP/DOWN平均値)
        upema = up.ewm(span=span,adjust=False).mean()
        downema = down.ewm(span=span,adjust=False).mean()

        # spanの間の上昇率・下落率
        df[colNameUp] = upema / df[OPEN_]
        df[colNameDown] = downema / df[OPEN_]

        return df

    # EMAの計算
    # データフレームに新規列(項目名:colName)を作成しspanで指定したEMAを入れる
    # 引数で渡すデータフレームはローソク足データを想定
    @staticmethod
    def CalcEMA(df,span,colName):
        # 終値を指定期間でEMA計算。1行で出来るとかすげーわ
        df[colName] = df[CLOSE_].ewm(span=span,adjust=False).mean()

        # デバッグ用
        #print(df.loc[:,['openTime','close','EMA']])

        return df  

    # 変動率の計算
    # colname:格納する列名
    @staticmethod
    def CalcChangeRate(df,colName):
        # 変動率(%) ＝ (終値 / 始値) ＊ 100
        df[colName] = (df[CLOSE_]/df[OPEN_] * 100) - 100
        return df

    # 10日間の変動率(絶対値)のMAX
    # colChangeRate:変動率が入っている列名
    # colname:格納する列名
    @staticmethod 
    def CalcMaxChangeRate10(df,colChangeRate,colName):
        df[colName] = df[colChangeRate].abs().rolling(window=10,center=False).max()
        #l = [df['openTime'],df[colChangeRate],df[colName]]
        #print(l)
        return df

    @staticmethod 
    def CalcMaxMinChangeRate10(df,colChangeRate,colNameMax,colNameMin):
        df[colNameMax] = df[colChangeRate].rolling(window=10,center=False).max()
        df[colNameMin] = df[colChangeRate].rolling(window=10,center=False).min()
        #l = [df['openTime'],df[colChangeRate],df[colName]]
        #print(l)
        return df

    # BTCとの仲良し率(上昇連動率・下落連動率)
    # dfBTC:BTCローソク足データ
    # dfALT:ALTローソク足データ
    # colNameUpRate:UpRateが入っている列名
    # colNameDownRate:DownRateが入っている列名
    # colUpFriendRate:上昇連動率を入れる列名
    # colDownFriendRate:下落連動率を入れる列名
    @staticmethod
    def CalcBTCFriendRate(dfBTC,dfALT,colNameUpRate,colNameDownRate,colUpFriendRate,colDownFriendRate):
        # 上昇連動率計算
        dfALT[colUpFriendRate] = dfALT[colNameUpRate]/dfBTC[colNameUpRate]*100
        # 下落連動率計算
        dfALT[colDownFriendRate] = dfALT[colNameDownRate]/dfBTC[colNameDownRate]*100
        return dfALT

    @staticmethod
    def CalcRSI14Based4Hours(df):
        df = df[::-1]
        df4 = df[0::4]
        df4 = df4[::-1]
        diff = df4[CLOSE_].diff()

        # 差分データをとりあえず upとdown (データフレーム型)として放り込む
        up,down = diff.copy(),diff.copy()
        
        # up は差分がマイナスの行は0 downは差分がプラスの行は0とする 
        up[up < 0] = 0
        down[down > 0] = 0
        
        # 指数平滑移動平均でUPEMAとDOWNEMAを計算する。(単位時間当たりのUP/DOWN平均値)
        upema = up.ewm(span=14,adjust=False).mean()
        downema = down.ewm(span=14,adjust=False).mean()

        # 指数平滑移動平均で計算する。downの方はマイナス値なので絶対値とってから計算
        upema = up.ewm(13).mean()
        downema = down.abs().ewm(13).mean()

        if len(df4) > 14:
            # RSI計算して新しい列に放り込む
            df4['rsi14'] = upema/(upema+downema)*100
            rsi14 = df4.iloc[-1]['rsi14']
        else:
            rsi14 = 0

        return rsi14

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

def main():

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 全銘柄現在価格を取得
    dfTicker = GetViewData('VIEW_TICKER_INFO')
    dfTicker = dfTicker.set_index('symbol')
    dfTickerBTC = GetViewData('VIEW_TICKER_INFO_SPOT_BTC')
    dfTickerBTC = dfTickerBTC.set_index('symbol')
    #print(dfTicker.loc['BTCUSDT','price'])

    #'''
    # BTCのローソク足データ取得
    dfBTC = GetKlinesData('BINANCE_KLINES_1HOUR',"BTCUSDT",100)

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # テクニカル演算のリストを作成
    calcList = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]
        btcPair = pair.replace('USDT','BTC')
        point = symbol[1]

        # 最終価格を取得       
        lastPrice = dfTicker.loc[pair,PRICE_]
        lastPriceBTC = 0.0
        if btcPair in dfTickerBTC.index:
            lastPriceBTC = dfTickerBTC.loc[btcPair,PRICE_]
                
        # ローソク足データを取得
        dfDays = GetKlinesData('BINANCE_KLINES_1DAY',pair,500)
        dfDaysBTC = GetKlinesData('BINANCE_KLINES_1DAY_BTC',btcPair,500)
        df1Hour = GetKlinesData('BINANCE_KLINES_1HOUR',pair,100)
        #df4Hour = GetKlinesData('BINANCE_KLINES_4HOUR',pair,100)
        df4Hour = GetKlinesData('BINANCE_KLINES_6HOUR',pair,100)

        # 最終値を現在値に置き換え
        dfDays.Close.iloc[-1] = lastPrice
        df1Hour.Close.iloc[-1] = lastPrice
        df4Hour.Close.iloc[-1] = lastPrice
        if btcPair in dfTickerBTC.index:
            dfDaysBTC.Close.iloc[-1] = lastPriceBTC
        
        # ビットコイン連動率計算
        df1Hour = Technical.GetFriendRate(df1Hour,dfBTC)

        # EMA計算
        # EMA(200)
        dfDays = Technical.CalcEMA(dfDays,200,EMA_200_)
        # EMA(100)
        dfDays = Technical.CalcEMA(dfDays,100,EMA_100_)
        # EMA(50)
        dfDays = Technical.CalcEMA(dfDays,50,EMA_50_)
        # EMA(200) ※BTC建て
        dfDaysBTC = Technical.CalcEMA(dfDaysBTC,200,EMA_200_)

        # EMA短期
        dfDays = Technical.CalcEMA(dfDays,7,EMA_S_)
        df4Hour = Technical.CalcEMA(df4Hour,7,EMA_S_)
        df1Hour = Technical.CalcEMA(df1Hour,7,EMA_S_)
        # EMA中期
        dfDays = Technical.CalcEMA(dfDays,25,EMA_M_)
        df4Hour = Technical.CalcEMA(df4Hour,25,EMA_M_)
        df1Hour = Technical.CalcEMA(df1Hour,25,EMA_M_)

        # 9時からの変動率
        dfDays = Technical.CalcChangeRate(dfDays,CHANGE_RATE_)

        # RSI計算
        dfDays = Technical.CalcRSI(dfDays,14,RSI_14_)
        df4Hour = Technical.CalcRSI(df4Hour,14,RSI_14_)
        df1Hour = Technical.CalcRSI(df1Hour,14,RSI_14_)

        ##### 現在値取り出し 

        EMA200BTC = 0.0
        if btcPair in dfTickerBTC.index:
            EMA200BTC = dfDaysBTC.iloc[-1][EMA_200_]

        d = {
            'pair' : pair,
            'calcTime' : now,
            'price' : lastPrice,

            # EMA
            'EMA200' : round(dfDays.iloc[-1][EMA_200_],point),
            'EMA100' : round(dfDays.iloc[-1][EMA_100_],point),
            'EMA50' : round(dfDays.iloc[-1][EMA_100_],point),
            'EMA200BTC' : round(EMA200BTC,8),

            'EMA_S_1D' : round(dfDays.iloc[-1][EMA_S_],point),
            'EMA_S_4H' : round(df4Hour.iloc[-1][EMA_S_],point),
            'EMA_S_1H' : round(df1Hour.iloc[-1][EMA_S_],point),
            'EMA_M_1D' : round(dfDays.iloc[-1][EMA_M_],point),
            'EMA_M_4H' : round(df4Hour.iloc[-1][EMA_M_],point),
            'EMA_M_1H' : round(df1Hour.iloc[-1][EMA_M_],point),

            # 乖離率
            'DREMA200' : round(Technical.DeviationRate(dfDays.iloc[-1][EMA_200_],lastPrice),2),
            'DREMA100' : round(Technical.DeviationRate(dfDays.iloc[-1][EMA_100_],lastPrice),2),
            'DREMA50' : round(Technical.DeviationRate(dfDays.iloc[-1][EMA_50_],lastPrice),2),
            'DREMA200BTC' : round(Technical.DeviationRate(EMA200BTC,lastPriceBTC),2),

            # RSI(14) 4時間のRSI(14)
            'RSI14_1D' : round(dfDays.iloc[-1][RSI_14_],2),
            'RSI14_4H' : round(df4Hour.iloc[-1][RSI_14_],2),
            'RSI14_1H' : round(df1Hour.iloc[-1][RSI_14_],2),

            # 現在の変動率
            'ChangeRate' : round(dfDays.iloc[-1][CHANGE_RATE_],2),

            # BTC連動率(24時間)
            'BTCFRUp' : round(df1Hour.iloc[-1][FRIEND_RATE_UP_],2),
            'BTCFRDown' : round(df1Hour.iloc[-1][FRIEND_RATE_DOWN_],2),

        }

        calcList.append(d)

    return calcList




if __name__ == "__main__":
    calcList = main()
    '''
    for row in calcList:
        print(row)
    '''
    TechnicalInfo2db(calcList,'TECHNICAL_INFOS')

