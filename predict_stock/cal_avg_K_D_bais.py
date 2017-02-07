'''

Save file at /data/k_d_avg/
Every line is :

date, volume, money, open, high, low, close, diff, count, k, d, MA_5, MA_10, MA_15, MA_20, MA_40, MA_60, MA_120, RSI_6, RSI_9, RSI_14, RSI_24, BIAS_5, BIAS_10

'''

import os
import re
import sys
import string
import time
import argparse
import numpy as np
from datetime import datetime, timedelta

from os import mkdir
from os.path import isdir

src='/data/original'
target='/data/k_d_avg'
recover='/data/recover'
feat='/data/feat'
LAST_DAY = '93/02/11'
stock_history = {}
N = 9  # RSV
time_window = 25  # For Aroon index
ma_list = [5, 10, 15, 20, 40, 60, 120]
rsi_list = [6, 9, 14, 24]
bias_list = [5, 10]

def yesterday(date):
	yy, mm, dd = date.split('/')
	yesterday = datetime(int(yy)+1911, int(mm), int(dd)) - timedelta(1)

	return str(yesterday.year-1911)+'/'+str(yesterday.month).zfill(2)+'/'+str(yesterday.day).zfill(2)

def tomorrow(date):
	yy, mm, dd = date.split('/')
	yesterday = datetime(int(yy)+1911, int(mm), int(dd)) + timedelta(1)

	return str(yesterday.year-1911)+'/'+str(yesterday.month).zfill(2)+'/'+str(yesterday.day).zfill(2)

def interval_max_index(array, start, end):
	max_index = start
	m = array[start]
	for i in range(start, end):
		if array[i] >= m:
			m = array[i]
			max_index = i
	return max_index


def interval_min_index(array, start, end):
	min_index = start
	m = array[start]
	for i in range(start, end):
		if array[i] <= m:
			m = array[i]
			min_index = i
	return min_index


def RSV(close, highest, lowest, N):
	rsv = []
	max_n = []
	min_n = []
	for i in range(len(highest)):
		if i < N:
			max_n.append(max(highest[0:i+1]))
		else:
			max_n.append(max(highest[i-N+1:i+1]))
	for i in range(len(lowest)):
		if i < N:
			min_n.append(min(lowest[0:i+1]))
		else:
			min_n.append(min(lowest[i-N+1:i+1]))
		
	for i in range(len(close)):
		if max_n[i] == min_n[i]:
			rsv.append('nan')
		else:
			rsv.append((close[i] - min_n[i])/(max_n[i] - min_n[i])*100)
	
	return rsv

def K_value(rsv):
	k_value = []
	k_value.append(50.0)
	for i in range(1,len(rsv)):
		k_value.append(2*k_value[i-1]/3 + rsv[i]/3)

	return k_value

def D_value(k_value):
	d_value = []
	d_value.append(50.0)
	for i in range(1,len(k_value)):
		d_value.append(2*d_value[i-1]/3 + k_value[i]/3)

	return d_value

def moving_avg(close, ma):
	MA = []
	for i in range(len(close)):
		if i < ma:
			MA.append(sum(close[0:i+1])/len(close[0:i+1]))
		else:
			MA.append(sum(close[i-ma+1:i+1])/len(close[i-ma+1:i+1]))

	return MA

def RSI_index(diff, rsi_num):
	rsi = []
	for i in range(len(diff)):
		if i < rsi_num:
			pos = sum(x for x in diff[0:i+1] if x > 0)
			neg = abs(sum(x for x in diff[0:i+1] if x < 0))
			if pos+neg == 0:
				rsi.append(0)
			else:
				rsi.append(pos/(pos+neg)*100)
		else:
			pos = sum(x for x in diff[i-rsi_num+1:i+1] if x > 0)
			neg = abs(sum(x for x in diff[i-rsi_num+1:i+1] if x < 0))
			if pos+neg == 0:
				rsi.append(0)
			else:
				rsi.append(pos/(pos+neg)*100)
	return rsi

def BIAS_index(close, MA):
	bias = []
	for i in range(len(close)):
		if (close[i]+MA[i]) != 0:
			bias.append(close[i]/(close[i]+MA[i]))
		else:
			bias.append(0)

	return bias

def Aroon_index(close, window):
	up = []
	down = []
	osc = []
	for i in range(len(close)):
		if i < window:
			up.append(float(i-interval_max_index(close, 0, i+1))/window*100.0)
			down.append(float(i-interval_min_index(close, 0, i+1))/window*100.0)
			
		else:
			up.append(float(i-interval_max_index(close, i+1-window, i+1))/window*100.0)
			down.append(float(i-interval_min_index(close, i+1-window, i+1))/window*100.0)
		osc.append(up[i]-down[i])
	return up, down, osc



def main():
	file_names = os.listdir(src)

	for file_name in file_names:
		if not file_name.endswith('.csv'):
			continue
		
		print 'Processing ' + file_name
		with open('{}/{}'.format(src, file_name), 'rb') as file:
			#initial 
			date = []
			volume = []
			money = []
			start = []
			highest = []
			lowest = []
			close = []
			diff = []
			count = []
			MA = {}
			RSI = {}
			BIAS = {}
			# construct array
			for line in file.readlines():
				tokens = line.strip().split(',')
				if '--' in tokens or '---' in tokens or ('' in tokens and tokens[7] != ''):
					continue
				date.append(tokens[0])
				volume.append(int(tokens[1]))
				money.append(int(tokens[2]))
				start.append(float(tokens[3]))
				highest.append(float(tokens[4]))
				lowest.append(float(tokens[5]))
				close.append(float(tokens[6]))
				diff.append(close[len(close)-1]-close[len(close)-2])
				count.append(int(tokens[8]))

			rsv = RSV(close, highest, lowest, N)
			if 'nan' not in rsv:
				k_value = K_value(rsv)
				d_value = D_value(k_value)
				aroon_up, aroon_down, aroon_osc = Aroon_index(close, time_window)
	
				for ma in ma_list:
					MA['MA_'+str(ma)] = moving_avg(close, ma)

				for rsi_num in rsi_list:
					RSI['RSI_'+str(rsi_num)] = RSI_index(diff, rsi_num)
				
				for b in bias_list:
					BIAS['BIAS_'+str(b)] = BIAS_index(close, MA['MA_'+str(b)])


				output = open(target+'/'+file_name, 'w')
				recfile = open(recover+'/'+file_name, 'w')
				featfile = open(feat+'/'+file_name, 'w')

				for i in range(len(date)):
					recfile.write(date[i]+','+str(volume[i])+','+str(money[i])+','+str(start[i])+','+str(highest[i])+','+str(lowest[i])+','+str(close[i])+','+str(diff[i])+','+str(count[i])+'\n')
					output.write(date[i]+','+str(k_value[i])+','+str(d_value[i]))
					featfile.write(str(start[i])+','+str(highest[i])+','+str(lowest[i])+','+str(close[i])+','+str(diff[i])+','+str(count[i])+','+str(k_value[i])+','+str(d_value[i]))
					for ma in ma_list:
						output.write(','+str(MA['MA_'+str(ma)][i]))
						featfile.write(','+str(MA['MA_'+str(ma)][i]))

					for rsi_num in rsi_list:
						output.write(','+str(RSI['RSI_'+str(rsi_num)][i]))
						featfile.write(','+str(RSI['RSI_'+str(rsi_num)][i]))

					for b in bias_list:
						output.write(','+str(BIAS['BIAS_'+str(b)][i]))
						featfile.write(','+str(BIAS['BIAS_'+str(b)][i]))
					output.write(','+str(aroon_up[i])+','+str(aroon_down[i])+','+str(aroon_osc[i]))
					featfile.write(','+str(aroon_up[i])+','+str(aroon_down[i])+','+str(aroon_osc[i]))

					output.write('\n')
					featfile.write('\n')
			output.close()
			recfile.close() 
			featfile.close()

if __name__ == '__main__':
	main()
