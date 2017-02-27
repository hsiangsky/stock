import pandas as pd
from StockDataBase import *
import numpy as np
import talib
import progressbar

stock = Stock()
start_time = '2016/01/01'
end_time = '2017/02/18'
stklist = stock.get_TWSE_no()

hold = {}
money = 0
cost = 0
max_return = -100000
best_strong = 0
best_stable = 0

bar = progressbar.ProgressBar(max_value=len(stklist))
count = 0

for strong in range(50,100,5):
    for stable in range(0,50,2):
        money = 0
        cost = 0
        count = 0
        for stk_no in stklist:
            hold[stk_no] = 0
            count += 1
            bar.update(count)
            if stk_no not in stock.get_stock_list():
                continue
            dif, dea, macd = stock.MACD(stk_no, start_time, end_time)
            aroonup, aroondown, aroonosc = stock.Aroon(stk_no, start_time, end_time)
            close = stock.get_stock_data(stk_no=stk_no, attr='ClosePrice', start=start_time, end=end_time)

            if len(aroonosc) != len(close):
                continue
            for t in range(1, len(close)):
                if macd[t] > 0 and macd[t-1] < 0 and aroonosc[t] > stable and aroonup[t] > strong:
#                   print 'Buy ' + str(stk_no) + ', price ' + str(close[t])
                    hold[stk_no] += 1
                    money -= close[t]
                    cost += close[t]

                if macd[t] < 0 and macd[t-1] > 0 and aroonosc[t] < -1*stable and aroondown[t] > strong and hold[stk_no] > 0:
#                   print 'Sell ' + str(stk_no) + ', price ' + str(close[t])
                    hold[stk_no] -= 1
                    money += close[t]

            if hold[stk_no] != 0:
#           print 'Hold ' + str(stk_no) + ': ' + str(hold[stk_no]) + ', sell price ' + str(close[-1])
                money += close[-1]*hold[stk_no]

        print 'Strong index: ' + str(strong) + ', stable index: ' + str(stable)
        print 'Total return: '+ str(money*100.0/cost) + ' %'

        if (money*100.0/cost) > max_return:
            max_return = money*100.0/cost
            best_strong = strong
            best_stable = stable

print 'Best strong index: ' + str(best_strong) + ', best stable index: ' + str(best_stable)
print 'Best return: ' + str(max_return)

