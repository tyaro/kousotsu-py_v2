
from setting import session
from BinanceTableModel import *
from const import *
import pandas

# ローソク足データをDBへ登録
def klinesData2db(df,tablename):
    
    if df.empty:
        return

    # SQL 重複はアップデート
    query = 'INSERT INTO %s (symbol,openTime,open,close,high,low,coinVolume,usdtVolume) \
            VALUES("%s","%s",%s,%s,%s,%s,%s,%s) \
            ON DUPLICATE KEY UPDATE \
            open=%s,close=%s,high=%s,low=%s,coinVolume=%s,usdtVolume=%s'

    # ローソク足をDBに登録
    for _,row in df.iterrows():
        query1 = query % (tablename,
           row[SYMBOL_],row[OPEN_TIME_],row[OPEN_],row[CLOSE_],row[HIGH_],row[LOW_],row[VOLUME_],row[QUOTE_ASSET_VOLUME_],
            row[OPEN_],row[CLOSE_],row[HIGH_],row[LOW_],row[VOLUME_],row[QUOTE_ASSET_VOLUME_]
            )
        ENGINE.execute(query1)

    return