from setting import session
from BinanceTableModel import *
from const import *
import pandas as pd
import datetime
import redis
import json
from DBUtil2 import *

def kousotsutan():

    df1 = GetViewData('VIEW_KOUSOTSU_METHOD')
    df2 = GetViewData('VIEW_TICKER_INFO')

    df = pd.merge(df1,df2,left_on='pair',right_on='symbol')
    df = df.drop(columns='pair')
    df = df.reindex(columns=[
        'symbol',
        'price',
        'kousotsuPrice1',
        'kousotsuPrice2',
        'kousotsuPrice3',
        'EntryPointLong',
        'EntryPointShort',
        'calcTime',
        'tickerTime'])

    df['calcTime'] = df['calcTime'].astype(str)
    df['tickerTime'] = df['tickerTime'].astype(str)

    d = df.to_dict(orient='index')
    #print(d)
    
    calcList = []
    for row in d:
        # calcList.append(d[row])
        dd = {
            'symbol':d[row]['symbol'],
            'price':str(d[row]['price']),
            'kousotsuPrice1':str(d[row]['kousotsuPrice1']),
            'kousotsuPrice2':str(d[row]['kousotsuPrice2']),
            'kousotsuPrice3':str(d[row]['kousotsuPrice3']),
            'EntryPointLong':str(d[row]['EntryPointLong']),
            'EntryPointShort':str(d[row]['EntryPointShort']),
            'calcTime':d[row]['calcTime'],
            'tickerTime':d[row]['tickerTime'],
        }
        calcList.append(dd)

    return json.dumps(calcList,ensure_ascii=False)

def main():
    client = redis.Redis(host='localhost',port=26379,db=0)

    key = 'kousotsutan'
    value = kousotsutan()
    print(value)
    client.set(key,value)

if __name__ == "__main__":
    main()