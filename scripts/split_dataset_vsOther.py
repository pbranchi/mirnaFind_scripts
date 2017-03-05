#! /usr/bin/env	python
import sys, re
import numpy as np
import random
from math import floor

whole = open(sys.argv[1], 'r')
whole_labels = open(sys.argv[2], 'r')
train = open(sys.argv[5], 'w+')
validation = open(sys.argv[6],'w+')
t_labels = open(sys.argv[7],'w+')
v_labels = open(sys.argv[8],'w+')
part_pos = [1881,352,88,652,642]
nr_pos= sum(part_pos)
nr_neg = int(sys.argv[4])
try:
    split_perc = float(sys.argv[10])
except:
    split_perc = 0.2 #0.1

try:
    balance = sys.argv[9]
    balance = True if balance.upper() == "TRUE" else False
except:
    balance=False
if balance:
    max_ = nr_pos if nr_pos < nr_neg else nr_neg
    max_pos=int(floor(max_*split_perc))
    max_neg=int(floor(max_*split_perc))
    max_neg_tr=max_-max_neg
    max_pos_tr=max_-max_pos
else:
    max_pos=int(floor(nr_pos*split_perc))
    max_neg=int(floor(nr_neg*split_perc))
    max_neg_tr=nr_neg-max_neg
    max_pos_tr=nr_pos-max_pos
    max_ = max_pos
print max_pos
print max_neg
print max_neg_tr
print max_pos_tr
print 'NR POS: '+str(nr_pos)
print 'NR neg: '+str(nr_neg)

#pos_list = random.sample(range(1760), 176)
#neg_list = random.sample(range(1760), 176)
pos_list=[]
pos_list_tr=[]
for idx, val in enumerate(part_pos):
	ratio = float(val)/float(nr_pos)
	print "Ratio: "+str(ratio)
	offset = sum(part_pos[:idx])
	print "Offset:  "+str(offset)
	print "Val: "+str(val)
	print "Max Pos: "+str(max_)
	print "MaxPoa * Ratio: "+str(max_*ratio)
	if balance:
		tot_list = [x + offset for x in random.sample(range(val), int(max_*ratio))]
	else:
		tot_list = [x + offset for x in range(val)]
	_pos_list = random.sample(tot_list, int(max_pos*ratio))
	_pos_list_tr = [i for i in tot_list if i not in pos_list]
	print "len _pos_list: "+str(len(_pos_list))
	pos_list += _pos_list
	pos_list_tr += _pos_list_tr

#not_pos_list = [item for item in range(nr_pos) if item not in pos_list]

#pos_list_tr = random.sample(not_pos_list, max_pos_tr)
print "lenposlist: "+str(len(pos_list))
neg_list = random.sample(range(nr_neg), max_neg)
neg_list_tr = random.sample([item for item in range(nr_neg) if item not in neg_list], max_neg_tr)
neg_list = [x+ (nr_pos+1) for x in neg_list]
neg_list_tr = [x+ (nr_pos+1) for x in neg_list_tr]
whole_list = pos_list + neg_list
whole_list_tr = pos_list_tr + neg_list_tr

counter = 0
header = False
for line in whole.readlines():
    if not header:
        print header
        header = True
        validation.write(line)
        train.write(line)
        continue
    if counter in whole_list:
        validation.write(line)
    elif counter in whole_list_tr:
        train.write(line)
    counter += 1
counter = 0
validation.close()
train.close()

for line in whole_labels:
    if counter in whole_list:
        v_labels.write(line)
    elif counter in whole_list_tr:
        t_labels.write(line)
    counter += 1
print counter
v_labels.close()
t_labels.close()    

