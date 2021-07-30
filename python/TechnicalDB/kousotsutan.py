from setting import session
from BinanceTableModel import *
from const import *
import pandas as pd
import datetime
import redis
import json
from DBUtil2 import *

SP_ = 'spoint'
LP_ = 'lpoint'
JUDGEMENT_ = 'Judgement'

# ジャッジメントですの
def Judgement(df):

    df[SP_]=0
    df[LP_]=0
    df[JUDGEMENT_] = ""

    # ショート推奨価格を上回っているか
    df.loc[df[PRICE_] > df[SHORT_ENTRY_POINT_],SP_] = 1  
    # ロング推奨価格を下回っているか
    df.loc[df[PRICE_] < df[LONG_ENTRY_POINT_],LP_] = 1  

    # ショートの場合RSI14が60を下回っていたら星追加
    df.loc[(df[SP_] > 0) & (df['RSI14_4H'] < 60),SP_] = 2  
    # ロングの場合RSI14が40を上回っていたら星追加
    df.loc[(df[LP_] > 0) & (df['RSI14_4H'] > 40),LP_] = 2  

    # EMAの条件 ショートの場合EMA200とBTC建てEMA200を下回っているかどうか判断
    df.loc[(df[SP_] > 1) & (df['DREMA200'] < 0) & (df['DREMA200BTC'] < 0),SP_] = 3
    # EMAの条件 ロングの場合EMA200とBTC建てEMA200を上回っているかどうか判断
    df.loc[(df[LP_] > 1) & (df['DREMA200'] > 0) & (df['DREMA200BTC'] > 0),LP_] = 3

    # EMA200を満たしているときにEMA100の条件を確認
    df.loc[(df[SP_] > 2) & (df['DREMA100'] < 0),SP_] = df[SP_] + 1
    df.loc[(df[LP_] > 2) & (df['DREMA100'] > 0),LP_] = df[LP_] + 1

    # EMA200を満たしているときにEMA50の条件を確認
    df.loc[(df[SP_] > 2) & (df['DREMA50'] < 0),SP_] = df[SP_] + 1
    df.loc[(df[LP_] > 2) & (df['DREMA50'] > 0),LP_] = df[LP_] + 1

    df.loc[df[SP_] > 0,JUDGEMENT_] = "S"
    df.loc[df[LP_] > 0,JUDGEMENT_] = "L"

    return df

def kousotsutan():

    df1 = GetViewData('VIEW_KOUSOTSU_METHOD')
    df1 = df1.rename(columns={'pair':'symbol'})
    df1 = df1.rename(columns={'calcTime':'calcTime1'})
    #df2 = GetViewData('VIEW_TICKER_INFO')
    df2 = GetViewData('VIEW_TECHNICAL_INFOS')
    df = pd.merge(df1,df2,left_on='symbol',right_on='pair')
    df = df.drop(columns='pair')
    df = Judgement(df)

    df = df.reindex(columns=[
        'symbol',
        'price',
        'kousotsuPrice1',
        'kousotsuPrice2',
        'kousotsuPrice3',
        'EntryPointLong',
        'EntryPointShort',
        'TREND',
        'EMA200',
        'EMA100',
        'EMA50',
        'EMA200BTC',
        'EMA_S_1D',
        'EMA_S_4H',
        'EMA_S_1H',
        'EMA_M_1D',
        'EMA_M_4H',
        'EMA_M_1H',
        'DREMA200',
        'DREMA100',
        'DREMA50',
        'DREMA200BTC',
        'RSI14_1D',
        'RSI14_4H',
        'RSI14_1H',
        'BTCFRUp',
        'BTCFRDown',
        'ChangeRate',
        'Judgement',
        'lpoint',
        'spoint',
        'calcTime1',
        'calcTime'])
    #print(df)
    
    df['calcTime1'] = df['calcTime1'].astype(str)
    df['calcTime'] = df['calcTime'].astype(str)
    df = df.astype(str)

    d = df.to_dict(orient='index')
    
    calcList = []
    for row in d:
        '''
        calcList.append(d[row])
        '''
        dd = {
            'symbol':d[row]['symbol'],
            'price':d[row]['price'],
            'kousotsuPrice1':d[row]['kousotsuPrice1'],
            'kousotsuPrice2':d[row]['kousotsuPrice2'],
            'kousotsuPrice3':d[row]['kousotsuPrice3'],
            'EntryPointLong':d[row]['EntryPointLong'],
            'EntryPointShort':d[row]['EntryPointShort'],
            'TREND':d[row]['TREND'],
            'DREMA200':d[row]['DREMA200'],
            'DREMA100':d[row]['DREMA100'],
            'DREMA50':d[row]['DREMA50'],
            'DREMA200BTC':d[row]['DREMA200BTC'],
            'RSI14_1D':d[row]['RSI14_4H'],
            'BTCFRUp':d[row]['BTCFRUp'],
            'BTCFRDown':d[row]['BTCFRDown'],
            'ChangeRate':d[row]['ChangeRate'],
            'Judgement':d[row]['Judgement'],
            'lpoint':d[row]['lpoint'],
            'spoint':d[row]['spoint'],
            'calcTime1':d[row]['calcTime1'],
            'calcTime':d[row]['calcTime'],
        }
        calcList.append(dd)
        #'''

    return json.dumps(calcList,ensure_ascii=False)

def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'kousotsutan'
    value = kousotsutan()
    print(value)
    client.set(key,value)

if __name__ == "__main__":
    main()