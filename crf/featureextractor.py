import sys
import re
import os
import string
import subprocess


def GetOrthographicFeatures(word):
    features = ''
    features += word.lower() + '\t'
    # prefix and suffix features
    if(len(word) >= 4):
        features += word[0:1].lower() + '\t'
        features += word[0:2].lower() + '\t'
        features += word[0:3].lower() + '\t'
        features += word[len(word)-1:len(word)].lower() + '\t'
        features += word[len(word)-2:len(word)].lower() + '\t'
        features += word[len(word)-3:len(word)].lower() + '\t'
    else:
        features += '-\t-\t-\t' + '-\t-\t-\t'
    #Substring features (don't seem to help)
    #for i in range(1,len(word)-2):
    #    for j in range(i+1,len(word)-1):
    #        features.append("substr=%s" % word[i:j])

    # Initial capitalization
    if re.search(r'^[A-Z]', word):
        features += '1\t'   
    else:
        features += '0\t'

    # All capital
    if re.match(r'^[A-Z]+$', word):
        features += '1\t'  #ALLCAP
    else:
        features += '0\t'

    # has digit
    if re.match(r'.*[0-9].*', word):
        features += '1\t'
    else:
        features += '0\t'
    
    # has dot
    if re.match(r'.*\..*', word):
        features += '1\t'
    else:
        features += '0\t'

    # has both digit and dot
    if re.match(r'.*[0-9].*', word) and re.match(r'.*\..*', word):
        features += '1\t'
    else:
        features += '0\t'
    # has () at the end
    if re.match(r'\(\)$', word):
        features += '1\t'
    else:
        features += '0\t'

    # contains underscore
    if re.match(r'.*\_.*', word):
        features += '1\t'
    else:
        features += '0\t'

    # has Capital inside
    if re.match(r'.*[\w\_]+[A-Z][\w\_]+.*', word):
        features += '1\t'
    else:
        features += '0\t'
    
    # has dash
    if re.match(r'.*-.*', word):
        features += '1\t'
    else:
        features += '0\t'
    
    return features



if __name__=='__main__':
    # read in annotated conll file
    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')
    for line in fin:
        line = line.strip()
        if line:
            (word, label) = line.split('\t')
            OrthographicFeatures = GetOrthographicFeatures(word)

            allfeatures = word + '\t' + OrthographicFeatures + label
            fout.write(allfeatures + '\n')
    fout.close()
    fin.close()
