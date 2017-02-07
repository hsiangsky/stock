#!/usr/bin/env/python

import sys
import numpy as np

flist = open(sys.argv[1], 'r')
validlist = open('/data/valid_list_2.txt', 'w')

INCALID = False

for line in flist:
	line = line.strip()
	INVALID = False
	f = open('/data/'+line, 'r')
	for l in f:
		tokens = l.strip().split(',')
		if '--' in tokens or '---' in tokens:
			INVALID = True
			break
	if(not INVALID):
		validlist.write(line+'\n')
	f.close()
flist.close()
validlist.close()
