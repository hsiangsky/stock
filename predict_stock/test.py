import pandas as pd
from datetime import datetime
from StockDataBase import *
import numpy as np
import talib
a = {}

a['B'] = {}
a['B']['a'] = 2
a['B']['b'] = 3
a['B']['c'] = 4
a['B']['d'] = 5

a['A'] = {}
a['A']['a'] = 1
a['A']['b'] = 2
a['A']['c'] = 3
a['A']['d'] = 4

a['C'] = {}
a['C']['a'] = 3
a['C']['b'] = 4
a['C']['c'] = 5
a['C']['d'] = 6


for data, row in a.items():
	print data

df = pd.DataFrame(a)
print('df: ')
print df

print('append')
tt = pd.DataFrame()
tt = pd.concat([tt,pd.DataFrame(df['C'], columns=['A'])], axis = 1)
print tt.loc['b':'d']

print('A rolling 2, show b to d')
print df['A'].rolling(window=2).mean().loc['b':'d']

print('A, b to d , list')
print df.loc['b':'d']['A'].tolist()

print('df to matrix')
print df.values.tolist()

print df.to_dict()
print df.to_dict(orient='list')


stock = Stock()
#print stock.get_stock_data('9962')
#close = stock.get_stock_data(attr='ClosePrice')
close = stock.get_stock_data(stk_no='9962', attr='ClosePrice')

avg = talib.SMA(np.array(close), timeperiod = 5)
print avg[:10]

ma = stock.MA('9962')
print ma[:10]

print stock.get_stock_list()

k ,d = stock.KD_value('9962')
print k
print d

print k/4

print stock.RSV('9962')



dif, dea, macd = stock.MACD('9962')
print dif[:30]
print dea[:30]
print macd[:30]
#print talib.MAX(np.array(close), 14)[:20]

#close = stock.get_stock_data('9962', 'ClosePrice')
#print len(close.values.tolist())
#print type(close.values)
#print close.values.shape
#print type(close.values.transpose()[0][1])
#real = [ float(x) for x in close.values]
#print type(real[0])
#real = np.array(real)
#print type(real[1])
#avg = talib.SMA(real, timeperiod=30)
#print avg
#print avg.shape
#print type(avg)
#print avg
#print len(avg.tolist())
