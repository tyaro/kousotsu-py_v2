import requests
import pandas as pd
import numpy as np
from const import *




# バイナンスAPI
class BinanceAPI:
    # エンドポイント定義
    endPointF = 'https://fapi.binance.com'  #先物取引エンドポイント
    endPointS = "https://api.binance.com"  #現物取引エンドポイント
     
    # 初期化
    # pair(str):通貨ペア
    def __init__(self):
        pass
    
    # ローソク足の取得(先物市場)
    # pair(str):通貨ペア
    # num(int):取得する数 MAX1500 データ数が2より大きいで正常判定しているので3以上の値を入れる
    # interval(str):1m,1h,1d
    # 戻り値：DataFrame形式(column付き) 日時はUTC+0基準
    @staticmethod
    def GetKlinesF(pair,num,interval):
        # ローソク足取得用URLパス
        path = '/fapi/v1/klines?symbol=' + pair + '&limit=' + str(num) + '&interval=' + interval
        # APIサーバから情報を取得
        response = requests.get(BinanceAPI.endPointF + path).json()
        # レスポンスデータをPandasデータフレームに変換
        df = BinanceAPI.getDataFrame(response)
        return df

    # ローソク足の取得(スポット市場)
    # pair(str):通貨ペア
    # num(int):取得する数 MAX1500 データ数が2より大きいで正常判定しているので3以上の値を入れる
    # interval(str):1m,1h,1d
    # 戻り値：DataFrame形式(column付き) 日時はUTC+0基準
    @staticmethod
    def GetKlinesS(pair,num,interval):
        # ローソク足取得用URLパス
        path = '/api/v3/klines?symbol=' + pair + '&limit=' + str(num) +'&interval=' + interval
        # APIサーバから情報を取得
        response = requests.get(BinanceAPI.endPointS + path).json()
        # レスポンスデータをPandasデータフレームに変換
        df = BinanceAPI.getDataFrame(response)
        return df

    # ローソク足(KLinesデータ)をPandasのデータフレームに変換
    # レスポンスデータ数2以下を取得エラーと見なす
    @staticmethod
    def getDataFrame(response):

        if not 'msg' in response:
            # とってきたデータには項目名が付いていないので、項目名を追加してpandasのデータフレームに放り込む
            df = pd.DataFrame(data=response,columns=KLINES_COLUMNS)

            # とってきたデータは文字列型なのでfloat型に直しておく
            df.Open = df.Open.astype(float) 
            df.Close = df.Close.astype(float) 
            df.High = df.High.astype(float) 
            df.Low = df.Low.astype(float) 

            # UNIX時間とかパッと見わけわからんので UTC+0 基準の時間にしておく
            df.OpenTime = pd.to_datetime(df.OpenTime,unit='ms')   
            df.CloseTime = pd.to_datetime(df.CloseTime,unit='ms')
        else:
            # エラーの場合は空データを返す
            df = pd.DataFrame(index=range(1),columns=KLINES_COLUMNS).fillna(0)

        return df

    # 先物取引市場で現在値取得
    # pair(str):通貨ペア文字列
    @staticmethod
    def getTickerF(pair):
        # 現在価格取得URLパス
        path = '/fapi/v1/ticker/24hr?symbol=' + pair
        # APIサーバから値を取得
        response = requests.get(BinanceAPI.endPointF + path).json()
        # 現在の最終価格を取り出す
        if LAST_PRICE_ in response.keys():
            value = float(response[LAST_PRICE_])
        else:
            value = np.nan

        return value

    # 現物取引市場で現在値取得
    # pair(str):通貨ペア文字列
    @staticmethod
    def getTickerS(pair):
        # 現在価格取得URLパス
        path = '/api/v3/ticker/price?symbol=' + pair
        # APIサーバから値を取得
        response = requests.get(BinanceAPI.endPointS + path).json()
        # 現在の最終価格を取り出す
        if PRICE_ in response.keys():
            value = float(response[PRICE_])
        else:
            value = np.nan

        return value
