import pandas as pd
from const import *

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

    # 7日間の変動率(絶対値)のMAX
    # colChangeRate:変動率が入っている列名
    # colname:格納する列名
    @staticmethod 
    def CalcMaxChangeRate10(df,colChangeRate,colName):
        df[colName] = df[colChangeRate].abs().rolling(window=10,center=False).max()
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