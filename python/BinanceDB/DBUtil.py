
from setting import session
from BinanceTableModel import *
from const import *
import pandas
import datetime

# ローソク足データをDBへ登録
def klinesData2db(df,tablename):
    
    if df.empty:
        return

    # SQL 重複はアップデート
    query = 'INSERT INTO %s (symbol,openTime,open,close,high,low,coinVolume,usdtVolume,takerBuyUsdtVolume) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s,%s) \
            ON DUPLICATE KEY UPDATE \
            open=%s,close=%s,high=%s,low=%s,coinVolume=%s,usdtVolume=%s,takerBuyUsdtVolume=%s'

    # ローソク足をDBに登録
    for _,row in df.iterrows():
        query1 = query % (tablename,
           row[SYMBOL_],row[OPEN_TIME_],row[OPEN_],row[CLOSE_],row[HIGH_],row[LOW_],row[VOLUME_],row[QUOTE_ASSET_VOLUME_],row[TAKER_BUY_QUOTE_ASSET_VOLUME_],
            row[OPEN_],row[CLOSE_],row[HIGH_],row[LOW_],row[VOLUME_],row[QUOTE_ASSET_VOLUME_],row[TAKER_BUY_QUOTE_ASSET_VOLUME_]
            )
        ENGINE.execute(query1)

    return


# TickerデータをDBへ登録
def TickerInfo2db(df,tablename):
    
    if df.empty:
        return

    # SQL 重複はアップデート
    query = 'INSERT INTO %s (symbol,tickerTime,price) \
            VALUES("%s","%s",%s) \
            ON DUPLICATE KEY UPDATE \
            price=%s'

    # TICKER INFOをDBに登録
    for _,row in df.iterrows():
        query1 = query % (tablename,row[SYMBOL_],row[TIME_],row[PRICE_],row[PRICE_])
        ENGINE.execute(query1)

    return

# TickerデータをDBへ登録
def DeleteTickerInfo(tablename):
    
    delDatetime = datetime.datetime.now() + datetime.timedelta(hours=-48)
    #delDatetime = datetime.datetime.now() + datetime.timedelta(minutes=-3)

    query = 'DELETE FROM %s WHERE tickerTime <= "%s"'

    # TICKER INFOをDBに登録
    query1 = query % (tablename,delDatetime)
    print("48時間前のデータを削除します",query1)
    ENGINE.execute(query1)

    return