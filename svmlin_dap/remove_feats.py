import numpy as np
import csv
import sys

def extract_feats(datafile, removfile, nfeat, outfile):
    print locals()
    # table with feats abundances 
    data = np.loadtxt(datafile, delimiter = '\t', dtype = str)
    # feats abundances (no names of samples, no header)
    data_ab = data[1:,1:].astype(np.float)

    #rank = np.loadtxt(rankedfile, delimiter = '\t', skiprows = 1, dtype = str)
    # list with features to remove (NO HEADER)
    remov_list = np.loadtxt(removfile, delimiter = '\t', dtype = str)
    #feats = remov_list[:, 1]
    #top_feats = feats[0:nfeat]
    # features to remove
    remov_feats = remov_list[:nfeat]

    print remov_feats.shape
    # identify position of features to remove inside table with feats abundances
    idx_del = []
    for i in range(0, nfeat):
        if remov_feats[i] in data[0,:].tolist():
            idx_del.append(data[0,:].tolist().index(remov_feats[i]))
        else:
            print '%s not in dataset' %remov_feats[i]

    # considering samples names in the new table
    #idx = [0] + idx
    idx = range(data.shape[1])
    # indexes of features to keep
    map(idx.remove, idx_del)
    filt_data = data[:, idx]

    # write new table
    outw = open(outfile, 'w')
    writer = csv.writer(outw, delimiter = '\t', lineterminator = '\n')
    for i in range(0, len(filt_data[:,0])):
        writer.writerow(filt_data[i,:])

    outw.close()


if __name__ == "__main__":
    if not len(sys.argv) == 5:
        print "Usage: %prog data.txt removfile nfeat outdata.txt"
        sys.exit(1)

    # file with all feats abundances (where selected feats have to be removed from)
    datafile = sys.argv[1]
    # file with features to remove
    removfile = sys.argv[2]
    # number of feat to remove
    nfeat = int(sys.argv[3])
    # file with abundances of the all features but the removed ones
    outfile = sys.argv[4]

    extract_feats(datafile, removfile, nfeat, outfile)
