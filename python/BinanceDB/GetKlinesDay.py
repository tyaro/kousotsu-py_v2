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
        # BTC建てのシンボル名取得
        btcPair = pair.replace('USDT','BTC')
        print(pair,btcPair,"のローソク足データ(1日足)を取得してDBに登録します")
        # バイナンスから10日分のローソク足を取得
        df = BinanceAPI.GetKlinesF(pair,10,'1d')
        dfBTC = BinanceAPI.GetKlinesF(btcPair,10,'1d')
        # 銘柄情報を追加
        df[SYMBOL_] = pair
        dfBTC[SYMBOL_] = btcPair
        # DBへ登録
        klinesData2db(df,'BINANCE_KLINES_1DAY')
        klinesData2db(dfBTC,'BINANCE_KLINES_1DAY_BTC')
        # 遅延
        time.sleep(1)


@timeout_decorator.timeout(600)
def main():

    print("ローソク足データ(1日足)を取得します")
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