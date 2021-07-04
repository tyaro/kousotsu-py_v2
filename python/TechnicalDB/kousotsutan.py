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
        calcList.append(d[row])
        '''
        dd = {
            'symbol':row['symbol'],
            'price':row['price'],
            'kousotsuPrice1':row['kousotsuPrice1'],
            'kousotsuPrice2':row['kousotsuPrice2'],
            'kousotsuPrice3':row['kousotsuPrice3'],
            'EntryPointLong':row['EntryPointLong'],
            'EntryPointShort':row['EntryPointShort'],
            'calcTime':row['calcTime'],
            'tickerTime':row['tickerTime'],
        }
        calcList.append(dd)
    '''
    return json.dumps(calcList,ensure_ascii=False)

def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'kousotsutan'
    value = kousotsutan()
    print(value)
    client.set(key,value)

if __name__ == "__main__":
    main()