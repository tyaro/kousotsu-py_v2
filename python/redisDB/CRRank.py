import redis
import json
from CRRank2 import ChangeRateRank

def main():
    client = redis.Redis(host='redis',port=6379,db=0)

    key = 'CR_Future'
    value = client.get(key)

    data = json.loads(value)

    sortedUprData1min = sorted(data,key=lambda x:float(x['CRate01']),reverse=True)
    sortedLwrData1min = sorted(data,key=lambda x:float(x['CRate01']))
    sortedUprData5min = sorted(data,key=lambda x:float(x['CRate05']),reverse=True)
    sortedLwrData5min = sorted(data,key=lambda x:float(x['CRate05']))
    sortedUprData10min = sorted(data,key=lambda x:float(x['CRate10']),reverse=True)
    sortedLwrData10min = sorted(data,key=lambda x:float(x['CRate10']))
    sortedUprData15min = sorted(data,key=lambda x:float(x['CRate15']),reverse=True)
    sortedLwrData15min = sorted(data,key=lambda x:float(x['CRate15']))
    sortedUprData30min = sorted(data,key=lambda x:float(x['CRate30']),reverse=True)
    sortedLwrData30min = sorted(data,key=lambda x:float(x['CRate30']))
    sortedUprData1hour = sorted(data,key=lambda x:float(x['CRate60']),reverse=True)
    sortedLwrData1hour = sorted(data,key=lambda x:float(x['CRate60']))
    sortedUprData4hour = sorted(data,key=lambda x:float(x['CRate240']),reverse=True)
    sortedLwrData4hour = sorted(data,key=lambda x:float(x['CRate240']))
    sortedUprData6hour = sorted(data,key=lambda x:float(x['CRate360']),reverse=True)
    sortedLwrData6hour = sorted(data,key=lambda x:float(x['CRate360']))
    sortedUprData8hour = sorted(data,key=lambda x:float(x['CRate480']),reverse=True)
    sortedLwrData8hour = sorted(data,key=lambda x:float(x['CRate480']))
    sortedUprData12hour = sorted(data,key=lambda x:float(x['CRate720']),reverse=True)
    sortedLwrData12hour = sorted(data,key=lambda x:float(x['CRate720']))
    sortedUprData24hour = sorted(data,key=lambda x:float(x['CRate1440']),reverse=True)
    sortedLwrData24hour = sorted(data,key=lambda x:float(x['CRate1440']))


    UCRRank1M = GetRankData(client,sortedUprData1min,'1M','CRate01')
    LCRRank1M = GetRankData(client,sortedLwrData1min,'1M','CRate01')
    UCRRank5M = GetRankData(client,sortedUprData5min,'1M','CRate05')
    LCRRank5M = GetRankData(client,sortedLwrData5min,'1M','CRate05')
    UCRRank10M = GetRankData(client,sortedUprData10min,'1M','CRate10')
    LCRRank10M = GetRankData(client,sortedLwrData10min,'1M','CRate10')
    UCRRank15M = GetRankData(client,sortedUprData15min,'15M','CRate15')
    LCRRank15M = GetRankData(client,sortedLwrData15min,'15M','CRate15')
    UCRRank30M = GetRankData(client,sortedUprData30min,'15M','CRate30')
    LCRRank30M = GetRankData(client,sortedLwrData30min,'15M','CRate30')
    UCRRank1H = GetRankData(client,sortedUprData1hour,'1H','CRate60')
    LCRRank1H = GetRankData(client,sortedLwrData1hour,'1H','CRate60')
    UCRRank4H = GetRankData(client,sortedUprData4hour,'4H','CRate240')
    LCRRank4H = GetRankData(client,sortedLwrData4hour,'4H','CRate240')
    UCRRank6H = GetRankData(client,sortedUprData6hour,'6H','CRate360')
    LCRRank6H = GetRankData(client,sortedLwrData6hour,'6H','CRate360')
    UCRRank8H = GetRankData(client,sortedUprData8hour,'6H','CRate480')
    LCRRank8H = GetRankData(client,sortedLwrData8hour,'6H','CRate480')
    UCRRank12H = GetRankData(client,sortedUprData12hour,'6H','CRate720')
    LCRRank12H = GetRankData(client,sortedLwrData12hour,'6H','CRate720')
    UCRRank24H = GetRankData(client,sortedUprData24hour,'1D','CRate1440')
    LCRRank24H = GetRankData(client,sortedLwrData24hour,'1D','CRate1440')


    setRedis(client,UCRRank1M,'UPR1M')
    setRedis(client,LCRRank1M,'LWR1M')
    setRedis(client,UCRRank5M,'UPR5M')
    setRedis(client,LCRRank5M,'LWR5M')
    setRedis(client,UCRRank10M,'UPR10M')
    setRedis(client,LCRRank10M,'LWR10M')
    setRedis(client,UCRRank15M,'UPR15M')
    setRedis(client,LCRRank15M,'LWR15M')
    setRedis(client,UCRRank30M,'UPR30M')
    setRedis(client,LCRRank30M,'LWR30M')
    setRedis(client,UCRRank1H,'UPR1H')
    setRedis(client,LCRRank1H,'LWR1H')
    setRedis(client,UCRRank4H,'UPR4H')
    setRedis(client,LCRRank4H,'LWR4H')
    setRedis(client,UCRRank6H,'UPR6H')
    setRedis(client,LCRRank6H,'LWR6H')
    setRedis(client,UCRRank8H,'UPR8H')
    setRedis(client,LCRRank8H,'LWR8H')
    setRedis(client,UCRRank12H,'UPR12H')
    setRedis(client,LCRRank12H,'LWR12H')
    setRedis(client,UCRRank24H,'UPR24H')
    setRedis(client,LCRRank24H,'LWR24H')

    ChangeRateRank(client)

def setRedis(client,value,dataName):
    key = 'CRRank_' + dataName
    value = json.dumps(value,ensure_ascii=False)
    client.set(key,value)

def GetRankData(client,sortedData,span,colName):
    rank = 1
    rankList = []
    for row in sortedData:
        pair = row['pair']
        key = 'Trend_Price_' + pair
        value = client.get(key)
        data = json.loads(value)
        price = {
            'Value':data['Value'],
            'Trend':data['Trend'][span],
        }
        info = {
            'Rank':rank,
            'Pair':pair,
            'CRate':row[colName],
            'Price':price,
        }
        rankList.append(info)
        rank = rank + 1
        if rank == 11:
            break

    return rankList


if __name__ == "__main__":
    main()
