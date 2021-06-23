from BinanceAPI import *
from setting import session
from BinanceTableModel import *
from const import *
import time
import timeout_decorator 
from DBUtil import TickerInfo2db,DeleteTickerInfo


def GetTickerF():
    # bainanceAPIから先物現在価格(全て)を取得
    # BUSDや4半期どうちゃらは不要
    df = BinanceAPI.GetTikcerPriceF()
    df = df[~df[SYMBOL_].str.contains('_')]
    df = df[~df[SYMBOL_].str.contains('BUSD')]
    df = df.sort_values(SYMBOL_)
    TickerInfo2db(df,'BINANCE_TICKER_INFO')
    DeleteTickerInfo('BINANCE_TICKER_INFO')

@timeout_decorator.timeout(40)
def main():
    print("全銘柄の現在価格を先物板から取得します(TICKER)")
    GetTickerF()

if __name__ == "__main__":

    try:
        main()
    except:
        print("処理がタイムアウトしました")
    else:
        print("正常終了しました")
