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

def ranking(client,span):
    key = 'Volume_Info_' + span
    value = client.get(key)

    data = json.loads(value)
    df = json_normalize(data)
    
    df,infoPV = Evaluation(df,'PV')
    setRankData(client,'VOLRANK',df,'PV',span)

    df,infoDV = Evaluation(df,'DV')
    setRankData(client,'VOLRANK',df,'DV',span)


def setRankData(client,key,value,colName,span):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    colName2 = colName + 'DV'
    colName3 = colName + 'RANK'
    cols = ['Pair', colName,colName2,colName3]
    df = pd.DataFrame(index=[], columns=cols)
    df['Pair'] = value.Pair
    df['VOL'] = value['PV']
    df['MED'] = value['MED']
    df['PVC'] = value['PVC']
    df['PDV'] = value['DV']
    df['Value'] = value[colName]
    df['VOLDV'] = value[colName2]
    df['RATIO'] = value['RATIO']
    df['Rank'] = value[colName3]
    df['SPAN'] = value['SPAN']
    df = df.drop([colName,colName2,colName3],axis=1)
    df = df.astype(str)
    d = df.to_dict(orient='records')
    info = {
        'Type':'Ranking',
        'Result':d,
        'calcTime':now,
    }
    key = 'VRank_' + colName + '_' + span
    setRedis(client,key,info)
 
    for row in d:
        key2 = key + '_' + row['Pair']
        info = {
            'Type':'Ranking',
            'Result':{
                'Pair':row['Pair'],
                'VOL':row['VOL'],
                'PVC':row['PVC'],
                'MED':row['MED'],
                'Value':row['Value'],
                'PDV':row['PDV'],
                'DV':row['VOLDV'],
                'RATIO':row['RATIO'],
                'Rank':row['Rank'],
                'SPAN':row['SPAN'],
                'calcTime':now,
            }
        }
        setRedis(client,key2,info)

def VolumeRanking(client):
    ranking(client,'15MIN')
    ranking(client,'1HOUR')
    ranking(client,'4HOUR')
    ranking(client,'6HOUR')
    ranking(client,'1DAY')


def setRedis(client,key,value):
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)
    #print(key,value)


def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    VolumeRanking(client)




if __name__ == "__main__":
    main()