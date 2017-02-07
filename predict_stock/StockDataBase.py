from grs import TWSEOpen
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
import sys
import talib
import progressbar
import time

def string_to_time(string):
    year, month, day = string.split('/')
    return datetime(int(year), int(month), int(day))


def time_to_string(dtime):
    return str(dtime.year)+'/'+str(dtime.month).zfill(2)+'/'+str(dtime.day).zfill(2)


def day_back(start, timeperiod):
    now = string_to_time(start)
    back = 0
    while back < timeperiod:
        now -= timedelta(1)
        if TWSEOpen().d_day(now):
            back += 1
    return time_to_string(now)


class Stock:   

    def __init__(self):
        print 'Loading stock data...'
        self.src = '/data/recover'
        self.file_names = os.listdir(self.src)
        self.total_stock = len(self.file_names)
        self.stock = {}
        self.count = 0
        bar = progressbar.ProgressBar(max_value=self.total_stock)
        for self.file_name in ['9962.csv', '2618.csv']:
            self.count += 1
            bar.update(self.count)
            if not self.file_name.endswith('.csv'):
                continue

            with open('{}/{}'.format(self.src, self.file_name), 'rb') as file:
                self.stknum = self.file_name.split('.')[0]
                temp = {}
                temp['Volume'] = {}
                temp['Money'] = {}
                temp['OpenPrice'] = {}
                temp['HighestPrice'] = {}
                temp['LowestPrice'] = {}
                temp['ClosePrice'] = {}
                temp['Different'] = {}
                temp['Count'] = {}
                for line in file.readlines():
                    tokens = line.strip().split(',')
                    yy, mm, dd = tokens[0].split('/')
                    tokens[0] = str(int(yy) + 1911) + '/' + mm + '/' + dd
                    temp['Volume'][tokens[0]] = float(tokens[1])
                    temp['Money'][tokens[0]] = float(tokens[2])
                    temp['OpenPrice'][tokens[0]] = float(tokens[3])
                    temp['HighestPrice'][tokens[0]] = float(tokens[4])
                    temp['LowestPrice'][tokens[0]] = float(tokens[5])
                    temp['ClosePrice'][tokens[0]] = float(tokens[6])
                    temp['Different'][tokens[0]] = float(tokens[7])
                    temp['Count'][tokens[0]] = float(tokens[8])
                self.stock[self.stknum] = pd.DataFrame(temp)
        print 'Done.'


    def get_stock_data(self, stk_no=None, attr=None, start='2008/01/01', end='2015/12/31'):
        if stk_no != None and attr == None: 
            return self.stock[stk_no].loc[start:end].to_dict(orient='list') #dict

        elif stk_no == None and attr != None:
            result = pd.DataFrame()
            key_list = []
            for key in self.stock:
                key_list.append(key)
                result = pd.concat([result,self.stock[key][attr]], axis=1)
            result.columns = key_list
            return result.loc[start:end].to_dict(orient='list') #dict

        elif stk_no != None and attr != None:
            if isinstance(stk_no, str):
                return np.array([float(x) for x in self.stock[stk_no][attr].loc[start:end].values]) #np.array
            elif isinstance(stk_no, list):
                result = pd.DataFrame()
                for no in stk_no:
                    result = pd.concat([result, self.stock[no][attr]], axis=1)
                result.columns = stk_no
                return result.loc[start:end].to_dict(orient='list') #dict
            else:
                raise Exception('Error input stock number(should be a string or list of string).')

        else:
            raise Exception('Lack of input.')


    def get_stock_list(self):
        return [key for key in self.stock] #list


    #MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
    def MA(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=5, matype=0):
        realstart = day_back(start, timeperiod)
        close = self.get_stock_data(stk_no, 'ClosePrice', realstart, end)
        return talib.MA(close, timeperiod, matype=matype)[timeperiod:] 


    def RSI(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=14):
        realstart = day_back(start, timeperiod)
        close = self.get_stock_data(stk_no, 'ClosePrice', realstart, end)
        return talib.RSI(close, timeperiod)[timeperiod:]


    def BIAS(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=5):
        realstart = day_back(start, timeperiod)
        ma = self.MA(stk_no, realstart, end, timeperiod)
        close = self.get_stock_data(stk_no, 'ClosePrice', start, end)
        bias = []
        for i in range(len(close)):
            if (close[i] + ma[i]) != 0:
                bias.append(close[i]/(close[i]+ma[i]))
            else:
                bias.append(0)
        return np.array(bias)


    def Aroon(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=14):
        realstart = day_back(start, timeperiod)
        high = self.get_stock_data(stk_no, 'HighestPrice', realstart, end)
        low = self.get_stock_data(stk_no, 'LowestPrice', realstart, end)
        aroonup, aroondown = talib.AROON(high, low, timeperiod)
        aroonosc = talib.SUB(aroonup, aroondown)
        return aroonup[timeperiod:], aroondown[timeperiod:], aroonosc[timeperiod:]


    def RSV(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=9):
        realstart = day_back(start, timeperiod)
        high = self.get_stock_data(stk_no, 'HighestPrice', realstart, end)
        low = self.get_stock_data(stk_no, 'LowestPrice', realstart, end)
        close = self.get_stock_data(stk_no, 'ClosePrice', realstart, end)
        Max = talib.MAX(high, timeperiod=timeperiod)
        Min = talib.MIN(low, timeperiod=timeperiod)
        return talib.DIV(close-Min, Max-Min)[timeperiod:]


    def KD_value(self, stk_no, start='2008/01/01', end='2015/12/31', timeperiod=9):
        rsv = self.RSV(stk_no, start, end, timeperiod)
        k_value = []
        d_value = []
        k_value.append(50.0)
        d_value.append(50.0)

        for i in range(1,len(rsv)):
            k_value.append(2*k_value[i-1]/3 + rsv[i]/3)

        for i in range(1,len(k_value)):
            d_value.append(2*d_value[i-1]/3 + k_value[i]/3)

        return np.array(k_value), np.array(d_value)


    def MACD(self, stk_no, start='2008/01/01', end='2015/12/31', fastperiod=12, slowperiod=26, signalperiod=9):
        longest_period = max(fastperiod, slowperiod)+signalperiod
        realstart = day_back(start, longest_period)
        high = self.get_stock_data(stk_no, 'HighestPrice', realstart, end)
        low = self.get_stock_data(stk_no, 'LowestPrice', realstart, end)
        close = self.get_stock_data(stk_no, 'ClosePrice', realstart, end)
        P = (high + low + 2*close)/4
        E_fast = talib.EMA(P, fastperiod)
        E_slow = talib.EMA(P, slowperiod)
        dif = E_fast - E_slow
        dea = talib.EMA(dif, signalperiod)
        macd = dif - dea 
        return dif[longest_period:], dea[longest_period:], macd[longest_period:]








