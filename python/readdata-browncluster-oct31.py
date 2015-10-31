# -*- coding: utf-8 -*-

import sys,os
import MySQLdb
import re
from HTMLParser import HTMLParser
from htmlentitydefs import entitydefs
from random import randint

import codecs
codecs.register_error('replace_against_space', lambda e: (u' ',e.start + 1))
#print unicode('ABC\x97ab\x99c上午', 'utf-8', errors='replace_against_space')
pl = ['java', 'javascript', 'c#', 
	   'php', 
	   'android', 
	   'jquery', 
	   'python', 
	   'html'
]

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i 

def my_encoder(my_string):
   for i in my_string:
      try :
         yield unicode(i, 'utf-8')
      except UnicodeDecodeError:
         yield ' ' #or another whietespaces 

def strip_backtick(istring):
    return re.sub(r'(`(?=\S)|(?<=\S)`)', '', istring)  # this is hacky. Deheng

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
        self.entityref = re.compile('&[a-zA-Z][-.a-zA-Z0-9]*[^a-zA-Z0-9]')
    
    def handle_data(self, d):
        self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        self.fed.append(' ')

    def handle_endtag(self, tag):
        self.fed.append(' ')
   
    def handle_entityref(self, name):
        if entitydefs.get(name) is None:
            m = self.entityref.match(self.rawdata.splitlines()[self.lineno-1][self.offset:])
            entity = m.group()
            # semicolon is consumed, other chars are not.
            if entity is not None:
            	#print "entity is none"
            	if entity[-1] != ';':
                	entity = entity[:-1]
            	self.fed.append(entity)
            else: 
            	self.fed.append('')
        else:
            self.fed.append(' ')

    def get_data(self):
        self.close()
        return ''.join(self.fed) 

def strip_tags(html):
    s = MLStripper()
    html = re.sub(r'&#xA;&#xA;<pre>.*?</pre>', '@codeSnippetRemoved', html)
    html = re.sub(r'(`(?=\S)|(?<=\S)`)', '', html)
    html = re.sub(r'(&#xA;&#xA;)+','\n', html)
    s.feed(html)
    return s.get_data()
mycompile = lambda pat:  re.compile(pat,  re.UNICODE)
WS_RE = mycompile(r'  +')
def squeeze_whitespace(s):
  new_string = WS_RE.sub(" ",s)
  return new_string.strip()

class DataReader:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", 
		                     user="root", 
		                     passwd="ydh0114", 
		                     db="stackoverflow201503")
		self.cur = self.db.cursor() 

	def generate_postid(self, annotator):

		fall = open('./' + str(annotator) + '/all-oct31.txt', 'w' )
		
		for name in pl: 
			index_list = []

			fname = './postid/' + name + 'postid.txt'
			flen = file_len(fname)

			if name in ['java', 'javascript']:
				rand_max = 150000
			elif name in ['php', 'c#']:
				rand_max = 120000
			elif name in ['android', 'jquery']:
				rand_max = 100000
			elif name in ['python', 'html']:
				rand_max = 80000

			print rand_max

			for i in range(rand_max):
				f = open(fname, 'r')
				lines = f.readlines()
				index = randint(0, flen)
				#print index_list
				if index not in index_list:
					try: 
						index_list.append(index)
						rand = lines[index] 

						f.close()

						row_count = self.cur.execute("SELECT Id FROM posts where Id=%s" % (rand))
						if row_count > 0: 
							postid = self.cur.fetchall()[0][0]

							self.cur.execute("SELECT Title FROM posts where Id=%s" % (postid))
							title = self.cur.fetchall()

							self.cur.execute("SELECT Body FROM posts where Id=%s" %(postid))
							body = self.cur.fetchall()
							if title[0][0] is None:
								all = body 
							else: 
								all = title + body  	
							
							self.cur.execute("SELECT Id FROM posts where ParentId=%s" %(postid))
							answers = self.cur.fetchall()
							for row in answers:
								answer_id = row[0]
								self.cur.execute("SELECT Body FROM posts where Id=%s" %(answer_id))
								ans_body = self.cur.fetchall()
								all += ans_body

							
							for row in all: 
								content = ''.join( my_encoder(strip_tags(row[0])) )
								content = re.sub(r'^ +', '', content)
								content = re.sub(r'\n +', '\n', content)
								content = re.sub(r'[\n]+', '\n',content)

								fall.write(content +'\n')
							fall.write('\n')
					except:
						pass
		fall.close()
	

	def read_post(self, post_id):
		self.cur.execute("SELECT Title FROM posts where Id=%s" % (post_id))
		title = self.cur.fetchall()

		self.cur.execute("SELECT Body FROM posts where Id=%s" %(post_id))
		body = self.cur.fetchall()
		#self.cur.execute("SELECT Text FROM comments where PostId=%s" % (post_id))
		#comments = self.cur.fetchall()
		
		if title[0][0] is None:
			all = body 
		else: 
			all = title + body 
			
		self.cur.execute("SELECT Id FROM posts where ParentId=%s" %(post_id))
		answers = self.cur.fetchall()
		for row in answers:
			answer_id = row[0]
			self.cur.execute("SELECT Body FROM posts where Id=%s" %(answer_id))
			ans_body = self.cur.fetchall()
			all += ans_body



		f = open('./rawdata/' + str(post_id)+'.txt', 'w' )
		for row in all: 
			content = strip_tags(row[0])+'\n'
			content = re.sub(r'^ +', '', content)
			content = re.sub(r'\n +', '\n', content)
			content = re.sub(r'[\n]+', '\n',content)

			f.write(content)
		f.close()

		return all



if __name__ ==  '__main__':
	r = DataReader()
	annotators = ['browncluster-oct31']
	for anno in annotators: 
		r.generate_postid(anno)
	#r.read_post('1661921')