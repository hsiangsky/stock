'''

K-means, cluster stock to 10 cluster

'''

import numpy as np
from sklearn.cluster import KMeans
import random
import sys
import os

feats = []
name = []
dim = 0
backtrack = 10
N_cluster = 10
FOLDER = '/data/feat'
exp = 'kmeans'
MODEL_SNAPSHOT = '/data/models/'+exp

if not os.path.exists(MODEL_SNAPSHOT):
    os.system('mkdir -p '+MODEL_SNAPSHOT)


file_names = os.listdir(FOLDER)

for file_name in file_names:

    if not file_name.endswith('.csv'):
        continue

    with open('{}/{}'.format(FOLDER,file_name), 'rb') as file:
        print file_name
        if os.stat('{}/{}'.format(FOLDER,file_name)).st_size == 0:
            continue
        temp = []
        avglist = []
        for line in file.readlines():
            tokens = line.strip().split(',')
            temp.append([ float(i) for i in tokens[:]])
        temp = np.array(temp)
        (row,col) = temp.shape
        for i in range(col):
            avg = np.mean(temp[:,i])
            std = np.std(temp[:,i])
            avglist.append(avg)
        name.append(file_name)
        feats.append(avglist)

X = np.array(feats)
kmeans = KMeans(n_clusters=N_cluster, random_state=7).fit(X)
label = kmeans.labels_
outfile = open(MODEL_SNAPSHOT+'/cluster.txt', 'w')
cluster = {}

for i in range(len(label)):
    if label[i] not in cluster:
        cluster[label[i]] = []
    cluster[label[i]].append(name[i])

for key in cluster:
    if not os.path.exists(MODEL_SNAPSHOT+'/Cluster_'+str(key)):
        os.system('mkdir -p '+MODEL_SNAPSHOT+'/Cluster_'+str(key))

    outfile.write('Cluster '+str(key)+':')
    print('Cluster '+str(key)+': '+str(len(cluster[key])))

    for i in range(len(cluster[key])):
        outfile.write(cluster[key][i])
        os.system('cp '+FOLDER+'/'+cluster[key][i]+' '+MODEL_SNAPSHOT+'/Cluster_'+str(key)+'/')
        if i != len(cluster[key])-1:
            outfile.write(',')
        else:
            outfile.write('\n')


