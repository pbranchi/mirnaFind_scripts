# sort features by their abundance
import numpy as np
import sys
import argparse
import csv

class myArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(myArgumentParser, self).__init__(*args, **kwargs)

    def convert_arg_line_to_args(self, line):
        for arg in line.split():
            if not arg.strip():
                continue
            if arg[0] == '#':
                break
            yield arg


parser = myArgumentParser(description='Create a feature list sorted by feature abundance (descending order)', 
fromfile_prefix_chars='@')
parser.add_argument('DATAFILE' ,type=str, help='Table samples X features')
parser.add_argument('OUTFILE', type=str, help='Output file')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
dataf = args.DATAFILE
outf = args.OUTFILE

datawh = np.loadtxt(dataf, delimiter='\t', dtype=str)
featname = datawh[0, 1:]
nfeat = len(featname)
data = datawh[1:, 1:].astype(np.float)

# sum features abundance across samples
sumfeat = np.sum(data, axis=0)
# sort features by abundance
sumfeat_sort = np.sort(sumfeat)[::-1]
# index of sorted features
idx_sort = np.argsort(sumfeat)[::-1]
# sorted features 
feat_sort = featname[idx_sort]

# write outputfile
of = open(outf, 'w')
of_w = csv.writer(of, delimiter='\t', lineterminator='\n')
of_w.writerow(['Feature', 'Total abundance'])
for i in range(nfeat):
	of_w.writerow([feat_sort[i], sumfeat_sort[i]])

of.close()