import sys

f = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')

for line in f:
    line = line.strip()
    if line:
        token = line.split()[3]
        tag = line.split()[0]
        f2.write(token + '\t' + tag + '\n')
    else:
        f2.write('\n')

f.close()
f2.close()
