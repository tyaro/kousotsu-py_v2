from BinanceTableModel import *
from setting import *
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

# ローソク足データをDBから取得
def GetRSIData(tablename,pair,span):

    query = 'select pair,calcTime,1min,15min,1hour,4hour,1day from %s where pair = "%s" order by calcTime desc limit %s'

    query1 = query % (tablename,pair,span)
    
    df = pd.read_sql_query(query1,con=ENGINE)
    #df = df.rename(columns={'openTime':OPEN_TIME_,'open':OPEN_,'close':CLOSE_,'high':HIGH_,'low':LOW_})
    df = df.iloc[::-1]
    return df

def GetKlinesCloseData(tablename,pair,span):

    query = 'select symbol,close from %s where symbol = "%s" order by openTime desc limit %s'

    query1 = query % (tablename,pair,span)
    
    df = pd.read_sql_query(query1,con=ENGINE)
    df = df.rename(columns={'close':CLOSE_})
    df = df.iloc[::-1]
    return df

def GetTicker(tablename,pair):
    query = 'select price from %s where symbol = "%s" order by tickerTime desc limit 1'
    query1 = query % (tablename,pair)
    df = pd.read_sql_query(query1,con=ENGINE)
    value = df.iloc[0][PRICE_]
    return value

def GetTickerData(tablename,pair,span):
    query = 'select symbol,price from %s where symbol = "%s" order by tickerTime desc limit %s'
    query1 = query % (tablename,pair,span)
    df = pd.read_sql_query(query1,con=ENGINE)
    value = df[::-1]
    return value

def GetSymbolList():
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)
    return symbolList

def main():
    pair = "ALICEUSDT"
    df = GetKlinesCloseData('BINANCE_KLINES_15MIN',pair,30)
    print(df)

if __name__ == "__main__":
    main()