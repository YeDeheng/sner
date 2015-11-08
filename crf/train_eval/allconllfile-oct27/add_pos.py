import sys, os
from itertools import izip

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
f3 = open(sys.argv[3], 'w')

for line1,line2 in izip(f1,f2):
    line1 = line1.rstrip()
    line2 = line2.rstrip()

    if line1:
        t1 = line1.split('\t')[0]
        t2 = line1.split('\t')[1]
        w1 = line2.split('\t')[0]
        w2 = line2.split('\t')[1]
        w3 = line2.split('\t')[2]

        newstr = w1+'\t'+w2+'\t'+t2+'\n'
        f3.write(newstr)
    else:
        f3.write('\n')
f1.close()
f2.close()
f3.close()

