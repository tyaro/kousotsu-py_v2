from BinanceAPI import *
from setting import session
from BinanceTableModel import *
from const import *
import time
import timeout_decorator 
from DBUtil import TickerInfo2db,DeleteTickerInfo


def GetTickerS():
    # bainanceAPIから先物現在価格(全て)を取得
    # BUSDや4半期どうちゃらは不要
    df = BinanceAPI.GetTikcerPriceS()
    df = df[df[SYMBOL_].str.endswith('USDT')]
    df = df[~df[SYMBOL_].str.endswith('UPUSDT')]
    df = df[~df[SYMBOL_].str.endswith('DOWNUSDT')]
    df = df.sort_values(SYMBOL_)
    TickerInfo2db(df,'BINANCE_TICKER_INFO_SPOT')
    DeleteTickerInfo('BINANCE_TICKER_INFO_SPOT')

@timeout_decorator.timeout(40)
def main():
    print("全銘柄の現在価格を現物板から取得します(TICKER)")
    GetTickerS()

if __name__ == "__main__":
    try:
        main()
    except:
        print("処理がタイムアウトしました")
    else:
        print("正常終了しました")
