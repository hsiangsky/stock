import pandas as pd
from StockDataBase import *
import numpy as np
from datetime import datetime
import talib
import progressbar

stock = Stock()
start_time = '2016/06/01'
end_time = '{0}/{1:02d}/{2:02d}'.format(datetime.today().year, datetime.today().month, datetime.today().day)
stklist = stock.get_TWSE_no()

long_list = []
short_list = []
strong = 50
stable = 30

print 'Analysis ' + end_time
bar = progressbar.ProgressBar(max_value=len(stklist))
count = 0

for stk_no in stklist:
    count += 1
    bar.update(count)
    if stk_no not in stock.get_stock_list():
        continue
    dif, dea, macd = stock.MACD(stk_no, start_time, end_time)
    aroonup, aroondown, aroonosc = stock.Aroon(stk_no, start_time, end_time)
    close = stock.get_stock_data(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)
    time_list = stock.get_time_series(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)

    if len(macd) != len(aroonosc) or len(macd) != len(close) or len(macd) < 30:
        continue
    if macd[-1] > 0 and macd[-2] < 0 and aroonosc[-1] > stable and aroonup[-1] > strong:
        long_list.append(stk_no)

    if macd[-1] < 0 and macd[-2] > 0 and aroonosc[-1] < -1*stable and aroondown[-1] > strong:
        short_list.append(stk_no)

print 'Long position:'        
print long_list
print 'Short position:'
print short_list


