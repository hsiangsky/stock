'''

Generate training and testing data
Save as feat_X label_y
Use open close high low volume ... etc as feature

'''

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop, SGD, Adam, Nadam

import numpy as np
import random
import sys
import os

## check if file existed
#if os.path.isfile('feat_X'):
#    print('feat_X existed, please check!!')
#    os._exit()
#if os.path.isfile('label_y'):
#    print('label_y existed, please check!!')
#    os._exit()

feats = []
dim = 0
backtrack = 10
FOLDER = '/data/models/kmeans/Cluster_7'
exp = 'test_no4'
MODEL_SNAPSHOT = '/data/models/'+exp

if not os.path.exists(MODEL_SNAPSHOT):
    os.system('mkdir -p '+MODEL_SNAPSHOT)


file_names = os.listdir(FOLDER)

for file_name in file_names:

    if not file_name.endswith('.csv'):
        continue

    with open('{}/{}'.format(FOLDER,file_name), 'rb') as file:
        if os.stat('{}/{}'.format(FOLDER,file_name)).st_size == 0:
            continue
        flag = 0
        temp = []
        for line in file.readlines():
            tokens = line.strip().split(',')
            temp.append([ float(i) for i in tokens[:]])
        temp = np.array(temp)
        (row,col) = temp.shape
        for i in range(col):
            avg = np.mean(temp[:,i])
            std = np.std(temp[:,i])
            if std == 0:
                flag = 1
            if std != 0:
                temp[:,i] = (temp[:,i] - avg)/std
            else:
                temp[:,i] = (temp[:,i] - avg)
        if flag == 0:
            for row in temp.tolist():
                feats.append(row)
        del temp
        file.close()


dim = len(feats[0])

X = np.zeros((len(feats)-backtrack, backtrack, dim))
Y = np.zeros((len(feats)-backtrack, 5))

buy = 0
up = 0
sell =0
down = 0
still = 0

for i in range(len(feats)-backtrack):
    X[i][:] = feats[i:i+backtrack]
    if feats[i+backtrack][4] > 0 and feats[i+backtrack-1][4] < 0:
        Y[i][0] = 1
        buy += 1
    elif feats[i+backtrack][4] > 0 and feats[i+backtrack-1][4] > 0:
        Y[i][1] = 1
        up += 1
    elif feats[i+backtrack][4] < 0 and feats[i+backtrack-1][4] > 0:
        Y[i][2] = 1
        sell += 1
    elif feats[i+backtrack][4] < 0 and feats[i+backtrack-1][4] < 0:
        Y[i][3] = 1
        down += 1
    else:
        Y[i][4] = 1
        still += 1

print('Total data: ',len(feats)-backtrack)
print('Buy: ',buy)
print('Up: ',up)
print('Sell: ', sell)
print('Down: ', down)
print('Still: ', still)

print X.shape

#cut = int((len(feats)-backtrack)*0.8)
#X_train = X[:cut]
#X_test = X[cut:]
#y_train = Y[:cut]
#y_test = Y[cut:]

# build model
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(backtrack, dim), activation='sigmoid', inner_activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(5))
model.add(Activation('softmax'))

optimizer = Nadam()
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

print('Training model...')

for itr in range(15):
    print('Iteration '+str(itr)+':')
    model.fit(X, Y, batch_size=32, nb_epoch=10,
              validation_split=0.2)
    model.save(MODEL_SNAPSHOT+'/model_itr_'+str(itr)+'.h5')

print('Evaluation...')
acc = model.evaluate(X_test, y_test, batch_size=32)

print()
print('ACC: ', acc)


