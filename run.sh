#!/bin/bash
#Get last 10 days data
python tsec/crawl.py -c

#Sort
echo "Sort data:"
python tsec/post_process.py

#Recover data
echo "Recovering data:"
python predict_stock/recover_data.py

#Select stock
echo "Selecting data:"
python predict_stock/arn_macd.py
