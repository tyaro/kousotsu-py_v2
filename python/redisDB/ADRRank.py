import redis
import json
import pandas as pd
from pandas import json_normalize
import datetime

def Evaluation(df,colName):
    colName2 = colName + 'DV'
    colName3 = colName + 'RANK'
    MED = round(df[colName].astype(float).median(),2)
    AVG = df[colName].astype(float).mean()
    STD = df[colName].astype(float).std()

    df[colName2] = round((df[colName].astype(float)-AVG)*10/STD + 50,2)
    #計算後に丸める
    AVG = round(AVG,2)
    STD = round(STD,2)

    df = df.sort_values(colName2, ascending=False)
    df[colName3] = df.reset_index().index +1

    d = {
        'MED':MED,
        'AVG':AVG,
        'STD':STD,
    }

    return df,d

def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'ARR_INFO'
    value = client.get(key)

    data = json.loads(value)
    df = json_normalize(data)
    
    df,infoARR0 = Evaluation(df,'ARR0')
    setRankData(client,'ADRR',df,'ARR0')

    df,infoARR5 = Evaluation(df,'ARR5')
    setRankData(client,'ADRR',df,'ARR5')

    df,infoARR10 = Evaluation(df,'ARR10')
    setRankData(client,'ADRR',df,'ARR10')

    df,infoARR20 = Evaluation(df,'ARR20')
    setRankData(client,'ADRR',df,'ARR20')

    df,infoARRE5 = Evaluation(df,'ARRE5')
    setRankData(client,'ADRR',df,'ARRE5')

    df,infoARRE10 = Evaluation(df,'ARRE10')
    setRankData(client,'ADRR',df,'ARRE10')

    df,infoARRE20 = Evaluation(df,'ARRE20')
    setRankData(client,'ADRR',df,'ARRE20')
    
    df = df.astype(str)
    d = df.to_dict(orient='records')

    calcList = {
        'ADRM':{
            'ADR0':str(infoARR0),
            'ADR5':str(infoARR5),
            'ADR10':str(infoARR10),
            'ADR20':str(infoARR10),
            'ADRE5':str(infoARRE5),
            'ADRE10':str(infoARRE10),
            'ADRE20':str(infoARRE20),
        }
    }
    setRedis(client,'ADRM',calcList)

def setRankData(client,key,value,colName):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    colName2 = colName + 'DV'
    colName3 = colName + 'RANK'
    cols = ['Pair', colName,colName2,colName3]
    df = pd.DataFrame(index=[], columns=cols)
    df['Pair'] = value.pair
    df['TDR'] = value['ARR0']
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
    key = 'ADRRank_' + colName
    setRedis(client,key,info)
    for row in d:
        key2 = key + '_' + row['Pair']
        info = {
            'Type':'Ranking',
            'Result':{
                'Pair':row['Pair'],
                'TDR':row['TDR'],
                'Value':row['Value'],
                'DV':row['DV'],
                'Rank':row['Rank'],
                'calcTime':now,
            }
        }
        setRedis(client,key2,info)

def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)





if __name__ == "__main__":
    main()