# -*- coding: utf-8 -*-
import sys
import re
import os
import string
import subprocess

def regex_or(*items):
    r = '|'.join(items)
    r = '(' + r + ')'
    return r
def pos_lookahead(r):
  return '(?=' + r + ')'
def optional(r):
  return '(%s)?' % r

def urlmatch(word):
    PunctChars = r'''['“".?!,(/:;]'''
    Entity = '&(amp|lt|gt|quot);'

    UrlStart1 = regex_or('https?://', r'www\.')
    CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca','edu','gov')
    UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
    UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
    UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
    UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$') # / added by Deheng

    Url = (r'\b' +
        regex_or(UrlStart1, UrlStart2) +
        UrlBody +
        pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))

    Url_RE = re.compile("(%s)" % Url, re.U|re.I)

    return Url_RE.match(word)

def GetOrthographicFeatures(word):

    dfs = ['java', 'js', 'jsp', 'xml', 'c', 'cpp', 'py', 'htm', 'html', 'com']
    ngram = 20

    features = ''
    features += word.lower() + '\t'
    features += word.upper() + '\t'
    # prefix and suffix features
    for i in range(1, ngram+1):
        if(len(word) >= i):
            features += word[0:i].lower() + '\t'
        else:
            features += '-\t'

    for i in range(1, ngram+1):
        if(len(word) >= i):
            features += word[len(word)-i:len(word)].lower() + '\t'
        else:
            features += '-\t'
    #Substring features (don't seem to help)
    #for i in range(1,len(word)-2):
    #    for j in range(i+1,len(word)-1):
    #        features.append("substr=%s" % word[i:j])

    # Initial capitalization
    if re.search(r'^[A-Z]', word):
        features += '1\t'
    else:
        features += '0\t'

    # All capital + digits
    if re.match(r'^[A-Z0-9]+$', word):
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

        parts = word.split('.')
        firstPart = parts[0]
        lastPart = parts[len(parts)-1]

        if lastPart not in dfs and firstPart is not None and len(firstPart)>1:
            features += '1\t'
        else:
            features += '0\t'
    else:
        features += '0\t'

    # has dot and Cap
    if re.match(r'.*\..*', word) and re.match(r'.*[A-Z].*', word):
        features += '1\t'
    else:
        features += '0\t'

    # has both digit and dot
    if re.match(r'.*[0-9].*', word) and re.match(r'.*\..*', word):
        features += '1\t'
    else:
        features += '0\t'

    # has () at the end
    if re.match(r'.*\(\)$', word):
        features += '1\t'
    else:
        features += '0\t'

    # contains underscore
    if re.match(r'.*\_.*', word):
        features += '1\t'
    else:
        features += '0\t'

    # has Capital inside + the word is [\w\_]
    if re.match(r'.*[\w\_]+[A-Z][\w\_]+.*', word) and re.match(r'^[\w\_]+$', word):
        features += '1\t'
    else:
        features += '0\t'

    # begin with dot but not followed by dfs
    if re.match(r'^\.\w+$', word):
        parts = word.split('.')
        lastPart = parts[1]

        if lastPart not in dfs:
            features += '1\t'
        else:
            features += '0\t'
    else:
        features += '0\t'

    # 2 API patterns
    if re.match(r'^[a-zA-Z\.\_][a-zA-Z\.\_]+$', word):
	features += '1\t'
    else:
	features += '0\t'

    if re.match(r'^(?:[a-zA-Z_][a-zA-Z_]+\.)+[a-zA-Z_][a-zA-Z_]+$', word):
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

    if len(path) > 5:
        features += path[:5] + '\t'
    else:
        features += path + '\t'
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

def GetGazetteerFeatures(word, AndroidClass, AndroidAPI, platforms, frams, stans, PLs, orgs, jQueryUIAPIs):
    features = ''

    if word.lower() in AndroidClass:
        features += 'isAndroidClass\t'
    else:
        features += 'notAndroidClass\t'

    if word.lower() in AndroidAPI:
        features += 'isAndroidAPI\t'
    else:
        features += 'notAndroidAPI\t'

    if word.lower() in platforms:
        features += 'isPlat\t'
    else:
        features += 'notPlat\t'

    if word.lower() in frams:
        features += 'isFram\t'
    else:
        features += 'notFram\t'

    if word.lower() in stans:
        features += 'isStan\t'
    else:
        features += 'notStan\t'

    if word.lower() in PLs:
        features += 'isPL\t'
    else:
        features += 'notPL\t'

    if word.lower() in orgs:
        features += 'isOrg\t'
    else:
        features += 'notOrg\t'

    if word.lower() in jQueryUIAPIs:
        features += 'isJQueryUI\t'
    else:
        features += 'notJQueryUI\t'
    return features


if __name__=='__main__':
    # read in annotated conll file

    f = open('paths', 'r')  # open word cluster file
    word_cluster_dict = {}
    for line in f:
        word_cluster_dict[line.split()[1]] = line.split()[0]
    f.close()

    AndroidClass = []
    f = open('../gazetteers/AndroidClassesPackages.txt', 'r')
    for line in f:
        line = line.strip()
        if line:
            AndroidClass.append(str(line).lower())
    f.close()

    AndroidAPI = []
    f = open('../gazetteers/AndroidMethods.txt', 'r')
    for line in f:
        line = line.strip()
        if line:
            AndroidAPI.append(str(line).lower())
    f.close()

    f = open('../gazetteers/PlatformList.txt', 'r')
    platforms = []
    for line in f:
        line = line.rstrip()
        if line:
            platforms.append(str(line).lower())
    f.close()

    f = open('../gazetteers/ToolLibraryFrameworkList.txt', 'r')
    frams = []
    for line in f:
        line = line.rstrip()
        if line:
            frams.append(str(line).lower())
    f.close()

    f = open('../gazetteers/SoftwareStandardList.txt', 'r')
    stans = []
    for line in f:
        line = line.rstrip()
        if line:
            stans.append(str(line).lower())
    f.close()

    f = open('../gazetteers/ProgrammingLanguageList.txt', 'r')
    pls = []
    for line in f:
        line = line.rstrip()
        if line:
            pls.append(str(line).lower())
    f.close()

    f = open('../gazetteers/SoftwareOrgs.txt', 'r')
    orgs = []
    for line in f:
        line = line.rstrip()
        if line:
            orgs.append(str(line).lower())
    f.close()

    f = open('../gazetteers/JQueryUIAPIs.txt', 'r')
    jQueryUIAPIs = []
    for line in f:
        line = line.rstrip()
        if line:
            jQueryUIAPIs.append(str(line).lower())
    f.close()

    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')

    for line in fin:
        line = line.strip()
        if line:
            (word, label) = line.split('\t')
            OrthographicFeatures = GetOrthographicFeatures(word)

            ClusterFeatures = GetWordClusterFeatures(word, word_cluster_dict)

            GazFeatures = GetGazetteerFeatures(word,AndroidClass, AndroidAPI, platforms, frams, stans, pls, orgs, jQueryUIAPIs)

            allfeatures = word + '\t' + OrthographicFeatures + ClusterFeatures + GazFeatures + label
            fout.write(allfeatures + '\n')
        else:
            fout.write('\n')
    fout.close()
    fin.close()
