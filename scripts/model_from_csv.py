#! /usr/bin/env	python


'''
SCRIPT PER CREARE IL MODELLO PARTENDO DAL FILE CSV CREATO DA MIRNAFE_TO_LIBLIN_NEW, CON FILTRO SU COLONNE CON TROPPI 0

args:
1 - positive csv
2 - negative csv
3 - output tab-separated
4 - output label file
5 - output comma-separated
6 - optional second negative file
'''


import pandas as pd
import numpy as np
import sys,re
try:
    pos = pd.read_csv(sys.argv[1], skipinitialspace=True,sep=",")
    pos['labels'] = "1"
except Exception as e:
    print e
    pos = None
try:
    neg = pd.read_csv(sys.argv[2],skipinitialspace=True,sep=",")
    neg['labels'] = "-1"
except Exception as e:
    print e
    neg = None
try:
    neg2 = pd.read_csv(sys.argv[6],skipinitialspace=True,sep=",")
    neg2['labels'] = "-1"
except Exception as e:
    print e
    neg2= None

common_cols = pos.columns.intersection(neg.columns)
res = pos[common_cols].append(neg[common_cols])
if neg2 is not None:
    res = res.append(neg2[common_cols])
res = res.fillna(0)
removed_columns = res.columns[(res == 0.0).all()]
res = res.ix[:, (res != 0.0).any()]
#res = res.drop('sequence_names',1)
labels = res['labels']
res = res.drop('labels',1)
for c in res.columns:
    if c == 'sequence_names':
        continue
    tot = len(res[c])
    not_0 = 0
    for d in res[c]:
        if float(d) != 0.0:
            not_0 += 1
    if float(not_0)/float(tot) < 0.8:  
        res = res.drop(c,1)    
res.to_csv(sys.argv[3], sep="\t",header=True, index=False)
#res.to_csv(sys.argv[5], sep=",",header=True, index=False)

print "LabelFile"+(sys.argv[5])
labfile = open(sys.argv[5], "w+")
#print len(res.columns)
for lab in labels:
    labfile.write(lab+"\n")
#for c in res.columns:
    #print c
    #pass
