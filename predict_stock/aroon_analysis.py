import pandas as pd
from StockDataBase import *
import numpy as np
import talib

stock = Stock()
start_time = '2016/01/01'
end_time = '2017/02/18'
stklist = stock.get_TWSE_no()

hold = {}
money = 0
max_money = -10000000
best_strong = 0
best_stable = 0
for strong in range(50,70,5):
    for stable in range(0,20,2):
        money = 0
        for stk_no in stklist:
            hold[stk_no] = 0
            if stk_no not in stock.get_stock_list():
                continue
            dif, dea, macd = stock.MACD(stk_no, start_time, end_time)
            aroonup, aroondown, aroonosc = stock.Aroon(stk_no, start_time, end_time)
            close = stock.get_stock_data(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)

            if len(macd) != len(aroonosc) or len(macd) != len(close):
                continue
            for t in range(1, len(close)):
                if macd[t] > 0 and macd[t-1] < 0 and aroonosc[t] > stable and aroonup[t] > strong:
#                   print 'Buy ' + str(stk_no) + ', price ' + str(close[t])
                    hold[stk_no] += 1
                    money -= close[t]

                if macd[t] < 0 and macd[t-1] > 0 and aroonosc[t] < -1*stable and aroondown[t] > strong and hold[stk_no] > 0:
#                   print 'Sell ' + str(stk_no) + ', price ' + str(close[t])
                    hold[stk_no] -= 1
                    money += close[t]

            if hold[stk_no] != 0:
#           print 'Hold ' + str(stk_no) + ': ' + str(hold[stk_no]) + ', sell price ' + str(close[-1])
                money += close[-1]*hold[stk_no]
        print 'Strong index: ' + str(strong) + ', stable index: ' + str(stable)
        print 'Total earn: '+str(money)
        if money > max_money:
            max_money = money
            best_strong = strong
            best_stable = stable

print 'Best strong index: ' + str(best_strong) + ', best stable index: ' + str(best_stable)
print 'Best earn money: ' + str(max_money)

