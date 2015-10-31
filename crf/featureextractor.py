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

def GetWordClusterFeatures(word, dict):
    features = ''
    if dict.has_key(word):
        path = str(dict.get(word))
    else:
        path = 'null'

    if len(path) > 6:
        features += path[:6] + '\t'
    else:
        features += path + '\t'
    if len(path) > 7:
        features += path[:7] + '\t'
    else:
        features += path + '\t'
    if len(path) > 8:
        features += path[:8] + '\t'
    else:
        features += path + '\t'
    if len(path) > 9:
        features += path[:9] + '\t'
    else:
        features += path + '\t'
    if len(path) > 10:
        features += path[:10]+ '\t'
    else:
        features += path + '\t'
    if len(path) > 11:
        features += path[:11] + '\t'
    else:
        features += path + '\t'
    if len(path) > 12:
        features += path[:12] + '\t'
    else:
        features += path + '\t'
    if len(path) > 13:
        features += path[:13] + '\t'
    else:
        features += path + '\t'
    if len(path) > 14:
        features += path[:14] + '\t'
    else:
        features += path + '\t'
    if len(path) > 15:
        features += path[:15] + '\t'
    else:
        features += path + '\t'
    #print features
    return features

def GetGazetteerFeatures(word, androidAPI, platforms):
    features = ''
    if word in androidAPI:
        #print word
        features += 'inAndroid\t'
    else:
        features += 'outAndroid\t'

    if word in platforms:
        features += 'isPlat\t'
    else:
        features += 'notPlat\t'
    return features


if __name__=='__main__':
    # read in annotated conll file

    f = open('paths', 'r')  # open word cluster file
    word_cluster_dict = {}
    for line in f:
        word_cluster_dict[line.split()[1]] = line.split()[0]
    f.close()

    f = open('../gazetteers/AndroidClassesPackages.txt', 'r')
    androidAPI = []
    for line in f:
        line = line.strip()
        if line:
            androidAPI.append(line)
    f.close()

    f = open('../gazetteers/PlatformList.txt', 'r')
    platforms = []
    for line in f:
        line = line.rstrip()
        if line:
            platforms.append(str(line).lower())
    f.close()

    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')

    for line in fin:
        line = line.strip()
        if line:
            (word, label) = line.split('\t')
            OrthographicFeatures = GetOrthographicFeatures(word)

            ClusterFeatures = GetWordClusterFeatures(word, word_cluster_dict)

            GazFeatures = GetGazetteerFeatures(word, androidAPI, platforms)

            allfeatures = word + '\t' + OrthographicFeatures + ClusterFeatures + GazFeatures + label
            fout.write(allfeatures + '\n')
        else:
            fout.write('\n')
    fout.close()
    fin.close()
