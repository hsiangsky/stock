'''

Save file at ~/data/recover
Ignore missing date data

'''

import os
import re
import sys
import string
import time
import argparse
import numpy as np
import progressbar
from datetime import datetime, timedelta

from os import mkdir
from os.path import isdir

src='/home/hsiangsky/stock/data/original'
recover='/home/hsiangsky/stock/data/recover'

def main():
	file_names = os.listdir(src)
	total_stock = len(file_names)
	progress = 0
	bar = progressbar.ProgressBar(max_value=total_stock)
	for file_name in file_names:
		progress += 1
		bar.update(progress)
		if not file_name.endswith('.csv'):
			continue
		
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

	
			recfile = open(recover+'/'+file_name, 'w')

			for i in range(len(date)):
				recfile.write(date[i]+','+str(volume[i])+','+str(money[i])+','+str(start[i])+','+str(highest[i])+','+str(lowest[i])+','+str(close[i])+','+str(diff[i])+','+str(count[i])+'\n')

			recfile.close()

if __name__ == '__main__':
	main()
