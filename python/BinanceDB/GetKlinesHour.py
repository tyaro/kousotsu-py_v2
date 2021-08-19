from setting import session
from BinanceTableModel import *
from BinanceAPI import *
import time
from DBUtil import klinesData2db
import timeout_decorator 

def getKlinesData(symbolList):

    # 全銘柄
    for symbol in symbolList:
        pair = symbol[0]
        #print(pair,"のローソク足データ(1時間足・4時間足)を取得してDBに登録します")
        # バイナンスから10日分のローソク足を取得
        df1h = BinanceAPI.GetKlinesF(pair,24,'1h')
        df4h = BinanceAPI.GetKlinesF(pair,24,'4h')
        df6h = BinanceAPI.GetKlinesF(pair,24,'6h')
        # 銘柄情報を追加
        df1h[SYMBOL_] = pair
        df4h[SYMBOL_] = pair
        df6h[SYMBOL_] = pair
        # DBへ登録
        klinesData2db(df1h,'BINANCE_KLINES_1HOUR')
        klinesData2db(df4h,'BINANCE_KLINES_4HOUR')
        klinesData2db(df6h,'BINANCE_KLINES_6HOUR')
        # 遅延
        time.sleep(1)


@timeout_decorator.timeout(600)
def main():

    print("ローソク足データ(1時間足・4時間足・6時間足)を取得します")
    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol)

    getKlinesData(symbolList)


if __name__ == "__main__":

    try:
        main()
    except:
        print("処理がタイムアウトしました")
    else:
        print("正常終了しました")