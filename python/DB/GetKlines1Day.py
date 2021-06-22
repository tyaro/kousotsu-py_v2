from setting import session
from BinanceTableModel import *
from BinanceAPI import *
import time
from DBUtil import klinesData2db


def main():

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol)

    # 全銘柄
    for symbol in symbolList:
        pair = symbol[0]
        print(pair)
        # バイナンスから10日分のローソク足を取得
        df = BinanceAPI.GetKlinesF(pair,10,'1d')
        # 銘柄情報を追加
        df[SYMBOL_] = pair
        # DBへ登録
        klinesData2db(df,'BINANCE_KLINES_1DAY')
        # 遅延
        time.sleep(0.5)


if __name__ == "__main__":
    main()