import pandas as pd
import numpy as np

stock=pd.read_csv('/data/original/2332.csv')

stock['ma'] = pd.rolling_mean(stock['45.50'],3)
print stock['ma']
