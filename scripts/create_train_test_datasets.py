#! /usr/bin/env	python
import os
import pandas as pd ##python pandas is required, install it with pip

ROOT= os.path.dirname(os.path.abspath(__file__))
PATH= ROOT+'/../datasets/mirnaNonMirna/raw'    ##controllare
OUTPUT_PATH = ROOT+'/../datasets/mirnaNonMirna/'   ##controllare
invalid_list = []#['all_hominidae','Homo_Sapiens','all_hominidae_wohs']

file_list = [PATH+"/"+f for f in os.listdir(PATH) if (os.path.isfile(PATH+"/"+f) and (f not in invalid_list))]
res_tr = pd.DataFrame()
res_ts = pd.DataFrame()
lab_tr = []
lab_ts = []
for f in file_list:
    df = pd.read_csv(f, skipinitialspace=True,sep=",", error_bad_lines=False, warn_bad_lines=True)
    df.set_index('sequence_names')
    train = df.sample(frac=0.5, random_state=200)
    test = df.drop(train.index)
    res_tr = res_tr.append(train, ignore_index=True)
    res_ts = res_ts.append(test, ignore_index=True)
    label = '1\n' if 'pos' in f else '-1\n'
    #print 'label: ' +label
    lab_tr += [label for i in train.index ]
    lab_ts += [label for i in test.index ]
cols=list(df.columns.values)
cols.pop(cols.index('sequence_names'))
res_tr = res_tr[['sequence_names']+cols]
res_ts = res_ts[['sequence_names']+cols]
res_tr = res_tr.fillna(0.0)
res_tr.to_csv(OUTPUT_PATH+'/train', sep="\t",header=True, index=False)
res_ts = res_ts.fillna(0.0)
res_ts.to_csv(OUTPUT_PATH+'/test', sep="\t",header=True, index=False)
res_ts.to_csv(OUTPUT_PATH+'/test', sep="\t",header=True, index=False)
with open(OUTPUT_PATH+'/test.labels', 'w+') as flab_ts:
    for l in lab_ts:
        flab_ts.write(l)
with open(OUTPUT_PATH+'/train.labels', 'w+') as flab_tr:
    for l in lab_tr:
        flab_tr.write(l)        
print "++ Finished  ++"
                
        
