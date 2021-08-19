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

    nowMin = datetime.datetime.now().strftime('%M')
    nowHour = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%H')
    k = float(nowMin)/60

    # テクニカル演算のリストを作成
    calcList = []

    for symbol in symbolList:
        pair = symbol[0]

        df = GetKlinesData('BINANCE_KLINES_1HOUR',pair,24*60)

        df[OPEN_TIME_] = df[OPEN_TIME_] + datetime.timedelta(hours=9)
        print(df)
        df1 = pd.DataFrame(index=[],columns=['time','vol'])
        df1['time'] = df[OPEN_TIME_].dt.strftime('%H')
        df1['vol'] = df[QUOTE_ASSET_VOLUME_].astype(float)
        # 現在時刻は現在分を60で割った数を平均値とする
        df1.loc[df1['time']==nowHour,'vol'] = df1['vol']*k

        df2= df1.groupby('time').mean()
        # 平均
        df2 = df2.rename(columns={'vol':'Avg'})
        df3 = df1.iloc[-25:-1]
        df3 = df3.set_index('time')
        # 標準偏差
        df2['std'] = df1.groupby('time').std()
        df2 = pd.merge(df2,df3,left_index=True,right_index=True,how='outer')

        # 偏差値
        df2['dev']=(df2['vol']-df2['Avg'])*10/df2['std']+50
        #print(df2)

        df4 = df2['dev']

        #print(df4)
        #df2.plot.bar()

        dfTemp = pd.DataFrame(index=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] ,columns=[])
        dfTemp = dfTemp.fillna(0)
        dfVol = pd.merge(dfTemp,df4,left_index=True,right_index=True,how='outer').fillna(0).astype(int)
        dfVol = dfVol.rename({'dev':pair},axis=1)
        #print(dfVol)
        d = dfVol.to_dict()

        calcList.append(d)

        info = parseData(calcList)
        print(info)
        break
        '''
        client = redis.Redis(host='localhost',port=26379,db=0)

        key = 'MarksHighPriceAnalysis'
        value = json.dumps(info1,ensure_ascii=False)
        client.set(key,value)
        key = 'MarksLowPriceAnalysis'
        value = json.dumps(info2,ensure_ascii=False)
        client.set(key,value)
        '''


if __name__ == "__main__":
    main()