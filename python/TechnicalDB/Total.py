from DBUtil2 import *
from const import *
import datetime
import redis
import json

def parseData(calcList):
    info = []
    k = ""
    for row in calcList:
        for key in row:
            for values in row.values():
                data = {
                    'pair':key,
                    '00':values['00'],
                    '01':values['01'],
                    '02':values['02'],
                    '03':values['03'],
                    '04':values['04'],
                    '05':values['05'],
                    '06':values['06'],
                    '07':values['07'],
                    '08':values['08'],
                    '09':values['09'],
                    '10':values['10'],
                    '11':values['11'],
                    '12':values['12'],
                    '13':values['13'],
                    '14':values['14'],
                    '15':values['15'],
                    '16':values['16'],
                    '17':values['17'],
                    '18':values['18'],
                    '19':values['19'],
                    '20':values['20'],
                    '21':values['21'],
                    '22':values['22'],
                    '23':values['23'],
                }
                info.append(data)
    return info



def main():

    # シンボルリストをDBから取得
    symbolList = session.query(BINANCE_SYMBOL_MASTER.symbol,BINANCE_SYMBOL_MASTER.point)

    # テクニカル演算のリストを作成
    calcList1 = []
    calcList2 = []
    # 全銘柄(5分/10分/30分/60分の変動率を計算)
    for symbol in symbolList:
        pair = symbol[0]

        df = GetKlinesData('BINANCE_KLINES_1HOUR',pair,24*60)
        df[OPEN_TIME_] = df[OPEN_TIME_] + datetime.timedelta(hours=9)
        df['time'] = df[OPEN_TIME_]
        df['date'] = df[OPEN_TIME_].dt.round("D")
        df = df.set_index(OPEN_TIME_)
        #ddf = df.groupby('time')['High'].max()
        highIndex = df['High'].groupby(pd.Grouper(freq='D')).idxmax()
        lowIndex = df['Low'].groupby(pd.Grouper(freq='D')).idxmin()
        dfHigh = df.loc[highIndex]
        dfLow = df.loc[lowIndex]
        
        dfHigh['time'] = dfHigh['time'].dt.strftime('%H')
        dfLow['time'] = dfLow['time'].dt.strftime('%H')

        dfTemp = pd.DataFrame(index=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] ,columns=[])
        dfTemp = dfTemp.fillna(0)

        dfHighCount = dfHigh['time'].value_counts().sort_index()
        dfLowCount = dfLow['time'].value_counts().sort_index()

        dfHighCount = pd.merge(dfTemp,dfHighCount,left_index=True,right_index=True,how='outer').fillna(0).astype(int)
        dfHighCount = dfHighCount.rename({'time':pair},axis=1)
        d1 = dfHighCount.to_dict()

        dfLowCount = pd.merge(dfTemp,dfLowCount,left_index=True,right_index=True,how='outer').fillna(0).astype(int)
        dfLowCount = dfLowCount.rename({'time':pair},axis=1)
        d2 = dfLowCount.to_dict()

        calcList1.append(d1)
        calcList2.append(d2)

        info1 = parseData(calcList1)
        info2 = parseData(calcList2)
        #print(info)

        client = redis.Redis(host='redis',port=6379,db=0)

        key = 'MarksHighPriceAnalysis'
        value = json.dumps(info1,ensure_ascii=False)
        client.set(key,value)
        key = 'MarksLowPriceAnalysis'
        value = json.dumps(info2,ensure_ascii=False)
        client.set(key,value)



if __name__ == "__main__":
    main()