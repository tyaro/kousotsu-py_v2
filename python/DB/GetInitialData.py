# バイナンスの先物板の通貨ペアと小数点位置をDBにマスタ登録します。
# 1日足・4時間足・1時間足のローソクデータをとってきます

from BinanceAPI import *
from setting import session
from BinanceTableModel import *
from const import *
import time
from DBUtil import klinesData2db


# 通貨ペアマスタテーブルのデータを取得
def GetSymbolData():
    # bainanceAPIから先物現在価格(全て)を取得
    # BUSDや4半期どうちゃらは不要
    df = BinanceAPI.GetTikcerPriceF()
    df = df.drop(columns=PRICE_)
    df = df[~df[SYMBOL_].str.contains('_')]
    df = df[~df[SYMBOL_].str.contains('BUSD')]
    df = df.sort_values(SYMBOL_)

    # 既にDB内に登録してあるシンボルは上書きする。なかったらInsert
    query = """INSERT INTO BINANCE_SYMBOL_MASTER (symbol,point,updatetime) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE point=%s ,updatetime=%s"""

    print("先物板通貨ペアを取得してDBにマスタデータとして登録します")
    print("※BUSDは除外します。")
    print("※永久のみです")
    for _,row in df.iterrows():
        # DFを分解して登録(既にDB内にあった場合は上書きする)
        ENGINE.execute(query,(row[SYMBOL_],row[POINT_],row[TIME_],row[POINT_],row[TIME_]))

    return df


# データベース初期セットアップ
def main():

    # 通貨ペアマスタテーブルのデータを取得
    df = GetSymbolData()

    # 全てのペアについてDBに登録する
    print("先物のローソク足を順次取得してデータベースに格納します")
    for pair in df[SYMBOL_]:
        
        # BTC建てのシンボル名取得
        btcPair = pair.replace('USDT','BTC')

        # ローソク足(1日)データ取得
        print(pair,"の1日ローソク足を1500件取得します")
        dfDays = BinanceAPI.GetKlinesF(pair,1500,'1d')
        dfDays[SYMBOL_] = pair
        klinesData2db(dfDays,'BINANCE_KLINES_1DAY')
        
        # BTC建てローソク足(1日)データ取得
        print(btcPair,"の1日ローソク足を1500件取得します")
        dfDaysBTC = BinanceAPI.GetKlinesS(btcPair,1500,'1d')
        dfDaysBTC[SYMBOL_] = btcPair
        klinesData2db(dfDaysBTC,'BINANCE_KLINES_1DAY_BTC')

        # ローソク足(4時間)データ取得
        print(pair,"の4時間足を1500件取得します")
        df4Hours = BinanceAPI.GetKlinesF(pair,1500,'4h')
        df4Hours[SYMBOL_] = pair
        klinesData2db(dfDays,'BINANCE_KLINES_4HOUR')

        # ローソク足(1時間)データ取得
        print(pair,"の1時間足ローソク足を1500件取得します")
        df1Hours = BinanceAPI.GetKlinesF(pair,1500,'1h')
        df1Hours[SYMBOL_] = pair
        klinesData2db(dfDays,'BINANCE_KLINES_1HOUR')
        
        # IP BANされないように遅延
        time.sleep(0.5)


if __name__ == "__main__":
    main()
