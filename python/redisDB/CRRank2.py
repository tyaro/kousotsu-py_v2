import redis
import json
import pandas as pd
from pandas import json_normalize
import datetime

def Evaluation(client,df,colName):
    colName2 = colName + 'DV'   #全体偏差値
    colName3 = colName + 'RANK' # 全体ランキング

    key = 'CRRank_MED_' +str(int(colName.replace('CRate',''))) + 'M'

    # 変動率の中央値・平均値・標準偏差・及び各銘柄の偏差値を求める
    MED = round(df[colName].astype(float).median(),2)
    AVG = df[colName].astype(float).mean()
    STD = df[colName].astype(float).std()
    df[colName2] = round((df[colName].astype(float)-AVG)*10/STD + 50,2)
    #偏差値計算後に丸める
    AVG = round(AVG,2)
    STD = round(STD,2)

    df = df.sort_values(colName2, ascending=False)
    df[colName3] = df.reset_index().index +1

    d = {
        'MED':str(MED),
        'AVG':str(AVG),
        'STD':str(STD),
    }
    setRedis(client,key,d)
    return df

def ChangeRateRank(client):
    key = 'CR_Future'
    value = client.get(key)

    data = json.loads(value)
    df = json_normalize(data)
    df = df.drop(['price.Trend','price.Value'],axis=1)

    #print(df)
    
    df = Evaluation(client,df,'CRate01')
    setRankData(client,df,'CRate01')
    df = Evaluation(client,df,'CRate05')
    setRankData(client,df,'CRate05')
    df = Evaluation(client,df,'CRate10')
    setRankData(client,df,'CRate10')
    df = Evaluation(client,df,'CRate15')
    setRankData(client,df,'CRate15')
    df = Evaluation(client,df,'CRate30')
    setRankData(client,df,'CRate30')
    df = Evaluation(client,df,'CRate60')
    setRankData(client,df,'CRate60')
    df = Evaluation(client,df,'CRate240')
    setRankData(client,df,'CRate240')
    df = Evaluation(client,df,'CRate360')
    setRankData(client,df,'CRate360')
    df = Evaluation(client,df,'CRate480')
    setRankData(client,df,'CRate480')
    df = Evaluation(client,df,'CRate720')
    setRankData(client,df,'CRate720')
    df = Evaluation(client,df,'CRate1440')
    setRankData(client,df,'CRate1440')

def setRankData(client,value,colName):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    colName2 = colName + 'DV'
    colName3 = colName + 'RANK'
    cols = ['Pair', colName,colName2,colName3]
    df = pd.DataFrame(index=[], columns=cols)
    df['Pair'] = value.pair
    df['Value'] = value[colName]
    df['DV'] = value[colName2]
    df['Rank'] = value[colName3]
    df = df.drop([colName,colName2,colName3],axis=1)
    df = df.astype(str)
    d = df.to_dict(orient='records')
    info = {
        'Type':'Ranking',
        'Result':d,
        'calcTime':now,
    }
    key = 'CRRank_' +str(int(colName.replace('CRate',''))) + 'M'
    setRedis(client,key,info)
    for row in d:
        key2 = key + '_' + row['Pair']
        info = {
            'Type':'Ranking',
            'Result':{
                'Pair':row['Pair'],
                'Value':row['Value'],
                'DV':row['DV'],
                'Rank':row['Rank'],
                'calcTime':now,
            }
        }
        setRedis(client,key2,info)

def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    #print(key,value)
    client.set(key,value)


def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    ChangeRateRank(client)


if __name__ == "__main__":
    main()