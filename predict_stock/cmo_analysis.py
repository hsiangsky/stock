import pandas as pd
from StockDataBase import *
import numpy as np
import talib
import progressbar
import sys
import os

stock = Stock()
start_time = '2016/01/01'
end_time = '2017/02/18'
stklist = stock.get_TWSE_no()
logfile = open('cmo.hl.log', 'w')

hold = {}
money = 0
cost = 0
max_return = -100000
best_window = 57
window = 57
best_high = 40
best_low = -48

bar = progressbar.ProgressBar(max_value=len(stklist))
count = 0

for high in range(40, 81, 2):
    for low in range(-80, -39, 2):
        money = 0
        cost = 0
        count = 0
        for stk_no in stklist:
            hold[stk_no] = 0
            count += 1
            bar.update(count)
            if stk_no not in stock.get_stock_list():
                continue
            cmo = stock.CMO(stk_no, start_time, end_time, window)
            if np.isnan(cmo).all():
                continue
            avg_cmo = talib.MA(np.array(cmo), timeperiod=14, matype=0)
            close = stock.get_stock_data(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)
            if len(cmo) != len(close):
                continue
            for t in range(1, len(close)):
                if (cmo[t] > low and cmo[t-1] < low):
                    print 'Buy ' + str(stk_no) + ', price ' + str(close[t])
                    logfile.write('Buy ' + str(stk_no) + ', price ' + str(close[t]) + '\n')
                    hold[stk_no] += 1
                    money -= close[t]
                    cost += close[t]

                if (cmo[t] > high or (cmo[t] < high and cmo[t-1] > high)) and hold[stk_no] > 0:
                    print 'Sell ' + str(stk_no) + ', price ' + str(close[t])
                    logfile.write('Sell ' + str(stk_no) + ', price ' + str(close[t]) + '\n')
                    hold[stk_no] += 1
                    hold[stk_no] -= 1
                    money += close[t]

            if hold[stk_no] != 0:
                print 'Hold ' + str(stk_no) + ': ' + str(hold[stk_no]) + ', sell price ' + str(close[-1])
                logfile('Hold ' + str(stk_no) + ': ' + str(hold[stk_no]) + ', sell price ' + str(close[-1]) + '\n')
                money += close[-1]*hold[stk_no]

        print 'High: ' + str(high) + '. Low: ' + str(low)
        logfile.write('High: ' + str(high) + '. Low: ' + str(low) + '\n')
        if cost == 0:
            print 'Empty buy list.'
            logfile.write('Total return: 0 %\n')
            continue
        print 'Total return: '+ str(money*100.0/cost) + ' %'
        logfile.write('Total return: '+ str(money*100.0/cost) + ' %\n')

        if (money*100.0/cost) > max_return:
            max_return = money*100.0/cost
            best_high = high
            best_low = low

#print 'Best window size: ' + str(best_window)
print 'High: ' + str(best_high) + '. Low: ' + str(best_low)
#print 'Total cost: ' + str(cost)
print 'Best return: ' + str(max_return) + ' %'
logfile.write('Best high: ' + str(best_high) + ', low: ' + str(best_low))
logfile.write('Best reture: '+ str(max_return))

