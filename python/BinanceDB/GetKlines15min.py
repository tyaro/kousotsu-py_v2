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
        #print(pair,"のローソク足データ(15分足)を取得してDBに登録します")
        # バイナンスから10日分のローソク足を取得
        df15min = BinanceAPI.GetKlinesF(pair,60,'15m')
        # 銘柄情報を追加
        df15min[SYMBOL_] = pair
        # DBへ登録
        klinesData2db(df15min,'BINANCE_KLINES_15MIN')
        # 遅延
        time.sleep(1)


@timeout_decorator.timeout(600)
def main():

    print("ローソク足データ(15分足)を取得します")
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
