# -*- coding: utf-8 -*-
import os
from mytokenizer import mytokenizer
import texttoconll
from os.path import basename
import subprocess

annotators = ['cheeyong', 'ziqun', 'xuejiao', 'lijing', 'chunyang', 'gaosa', 'deheng', 'liuyi']
for anno in annotators:
	rawdatadir = './annotation-oct20/' + anno + '/'
	for file in os.listdir(rawdatadir):
	    if file.endswith('.txt'):
			filebase = '.'.join(file.split('.')[:-1]) if '.' in file else file

			tokenfile = rawdatadir+str(file)+".tk"
			conllfile = rawdatadir+filebase+".conll"
			mytokenizer.tokenize(rawdatadir+str(file), tokenfile)
			texttoconll.main(tokenfile, conllfile)
			#subprocess.Popen("python conll02tostandoff.py -o ./rawdata/brat %s" % (conllfile), shell=True )
