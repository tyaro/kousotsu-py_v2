from BinanceAPI import *
from setting import session
from BinanceTableModel import *
from const import *
import time
import timeout_decorator 


def GetTickerF():
    # bainanceAPIから先物現在価格(全て)を取得
    # BUSDや4半期どうちゃらは不要
    df = BinanceAPI.GetTikcerPriceF()
    df = df[~df[SYMBOL_].str.contains('_')]
    df = df[~df[SYMBOL_].str.contains('BUSD')]
    df = df.sort_values(SYMBOL_)
    print(df)

@timeout_decorator.timeout(600)
def main():
    GetTickerF()


if __name__ == "__main__":
    main()

'''    try:
        main()
    except:
        print("処理がタイムアウトしました")
    else:
        print("正常終了しました")
        '''