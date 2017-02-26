import pandas as pd
from StockDataBase import *
import numpy as np
import talib

stock = Stock()
start_time = '2009/01/01'
end_time = '2010/01/01'
stklist = stock.get_TWSE_no()

hold = {}
money = 0
cost = 0
strong = 50
stable = 30

for stk_no in stklist:
    hold[stk_no] = 0
    if stk_no not in stock.get_stock_list():
        continue
    dif, dea, macd = stock.MACD(stk_no, start_time, end_time)
    aroonup, aroondown, aroonosc = stock.Aroon(stk_no, start_time, end_time)
    close = stock.get_stock_data(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)
    time_list = stock.get_time_series(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)

    if len(macd) != len(aroonosc) or len(macd) != len(close):
        continue
    for t in range(1, len(close)):
        if macd[t] > 0 and macd[t-1] < 0 and aroonosc[t] > stable and aroonup[t] > strong:
#            print time_list[t] + ', buy ' + str(stk_no) + ', price ' + str(close[t])
            hold[stk_no] += 1
            money -= close[t]
            cost += close[t]

        if macd[t] < 0 and macd[t-1] > 0 and aroonosc[t] < -1*stable and aroondown[t] > strong and hold[stk_no] > 0:
#            print time_list[t] + ', sell ' + str(stk_no) + ', price ' + str(close[t])
            hold[stk_no] -= 1
            money += close[t]

    if hold[stk_no] != 0:
#   print 'Hold ' + str(stk_no) + ': ' + str(hold[stk_no]) + ', sell price ' + str(close[-1])
        money += close[-1]*hold[stk_no]

print 'Cost: ' + str(cost)
print 'Earn money: ' + str(money)
print 'Return: ' + str(money*100.0/cost) + ' %'
