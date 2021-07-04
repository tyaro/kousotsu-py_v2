from setting import session
from BinanceTableModel import *
from const import *
import pandas as pd
import datetime

# ローソク足データをDBから取得
def GetKlinesData(tablename,pair,span):

    query = 'select symbol,openTime,open,close,high,low from %s where symbol = "%s" order by openTime desc limit %s'

    query1 = query % (tablename,pair,span)
    
    df = pd.read_sql_query(query1,con=ENGINE)
    df = df.rename(columns={'openTime':OPEN_TIME_,'open':OPEN_,'close':CLOSE_,'high':HIGH_,'low':LOW_})
    df = df.iloc[::-1]
    return df

def GetTicker(tablename,pair):
    query = 'select price from %s where symbol = "%s" order by tickerTime desc limit 1'
    query1 = query % (tablename,pair)
    df = pd.read_sql_query(query1,con=ENGINE)
    value = df.iloc[0][PRICE_]
    return value

def KousotsuMethod2db(calcList,tablename):

    if not calcList:
        return
    
    query = 'INSERT INTO %s \
            (pair,calctime,kousotsuPrice1,kousotsuPrice2,kousotsuPrice3,EntryPointLong,EntryPointShort) \
            VALUES("%s","%s",%s,%s,%s,%s,%s) \
            ON DUPLICATE KEY UPDATE \
            kousotsuPrice1=%s,kousotsuPrice2=%s,kousotsuPrice3=%s,EntryPointLong=%s,EntryPointShort=%s'

    for row in calcList:
        for k in row.keys():
            query1 = query % (
                tablename,
                row['pair'],
                row[CALC_TIME_],
                row[KOUSOTSU_PRICE_1_],
                row[KOUSOTSU_PRICE_2_],
                row[KOUSOTSU_PRICE_3_],
                row[LONG_ENTRY_POINT_],
                row[SHORT_ENTRY_POINT_],
                row[KOUSOTSU_PRICE_1_],
                row[KOUSOTSU_PRICE_2_],
                row[KOUSOTSU_PRICE_3_],
                row[LONG_ENTRY_POINT_],
                row[SHORT_ENTRY_POINT_])

            ENGINE.execute(query1)
    
    return

def GetViewData(viewName):
    query = 'select * from %s'
    query1 = query % (viewName)
    
    df = pd.read_sql_query(query1,con=ENGINE)
    return df



def main():
    '''
    df = GetKlinesData('BINANCE_KLINES_1DAY','BTCUSDT',20)
    value = GetTicker('BINANCE_TICKER_INFO','BTCUSDT')
    '''
    df1 = GetViewData('VIEW_KOUSOTSU_METHOD')
    df2 = GetViewData('VIEW_TICKER_INFO')
    df = pd.merge(df1,df2,left_on='pair',right_on='symbol')
    print(df)

if __name__ == "__main__":
    main()