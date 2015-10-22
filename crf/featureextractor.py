import sys
import re
import os
import string
import subprocess


def GetOrthographicFeatures(word):
    features = ''
    features += word.lower() + '\t'
    # if(len(word) >= 4):
    #     features.append("prefix=%s" % word[0:1].lower())
    #     features.append("prefix=%s" % word[0:2].lower())
    #     features.append("prefix=%s" % word[0:3].lower())
    #     features.append("suffix=%s" % word[len(word)-1:len(word)].lower())
    #     features.append("suffix=%s" % word[len(word)-2:len(word)].lower())
    #     features.append("suffix=%s" % word[len(word)-3:len(word)].lower())

        #Substring features (don't seem to help)
        #for i in range(1,len(word)-2):
        #    for j in range(i+1,len(word)-1):
        #        features.append("substr=%s" % word[i:j])

    if re.search(r'^[A-Z]', word):
        features += '1\t'   # capitalization
    else:
        features += '0\t'
    # if re.search(r'^[A-Z]', word) and goodCap:
    #     features.append('INITCAP_AND_GOODCAP')
    if re.match(r'^[A-Z]+$', word):
        features += '1\t'  #ALLCAP
    else:
        features += '0\t'
    # if re.match(r'^[A-Z]+$', word) and goodCap:
    #     features.append('ALLCAP_AND_GOODCAP')
    # if re.match(r'.*[0-9].*', word):
    #     features.append('HASDIGIT')
    # if re.match(r'[0-9]', word):
    #     features.append('SINGLEDIGIT')
    # if re.match(r'[0-9][0-9]', word):
    #     features.append('DOUBLEDIGIT')
    # if re.match(r'.*-.*', word):
    #     features.append('HASDASH')
    # if re.match(r'[.,;:?!-+\'"]', word):
    #     features.append('PUNCTUATION')
    return features

if __name__=='__main__':

    # read in annotated conll file
    fin = open('annotated.conll', 'r')
    fout = open('train.conll', 'w')
    for line in fin:
        line = line.strip()
        (word, label) = line.split('\t')
        OrthographicFeatures = GetOrthographicFeatures(word)

        allfeatures = word + '\t' + OrthographicFeatures + label
        fout.write(allfeatures + '\n')
    fout.close()
    fin.close()
