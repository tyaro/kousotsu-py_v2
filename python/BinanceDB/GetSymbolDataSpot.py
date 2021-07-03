from BinanceAPI import *
from setting import session
from BinanceTableModel import *
from const import *
import time

# 通貨ペアマスタテーブルのデータを取得
def GetSymbolData():
    # bainanceAPIから現物現在価格(USDTのみ)を取得
    # BUSDや4半期どうちゃらは不要
    df = BinanceAPI.GetTikcerPriceS()
    df = df[df[SYMBOL_].str.endswith('USDT')]
    df = df[~df[SYMBOL_].str.endswith('UPUSDT')]
    df = df[~df[SYMBOL_].str.endswith('DOWNUSDT')]
    df = df.sort_values(SYMBOL_)

    # 既にDB内に登録してあるシンボルは上書きする。なかったらInsert
    query = """INSERT INTO BINANCE_SYMBOL_MASTER_SPOT (symbol,point,updatetime) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE point=%s ,updatetime=%s"""

    print("現物板通貨ペアを取得してDBにマスタデータとして登録します")
    print("※USDTのみです")
    print("※UPDOWNトークンも除外")
    for _,row in df.iterrows():
        # DFを分解して登録(既にDB内にあった場合は上書きする)
        ENGINE.execute(query,(row[SYMBOL_],row[POINT_],row[TIME_],row[POINT_],row[TIME_]))

    return df

def main():
    # 通貨ペアマスタテーブルのデータを取得
    df = GetSymbolData()

if __name__ == "__main__":
    main()
