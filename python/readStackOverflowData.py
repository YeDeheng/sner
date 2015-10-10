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
            	print "entity is none"
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
    html = re.sub(r'<pre>.*?</pre>', ' ', html)
    html = re.sub(r'(`(?=\S)|(?<=\S)`)', '', html)
    html = re.sub(r'(&#xA;)+','\n', html)
    s.feed(html)
    return s.get_data()
mycompile = lambda pat:  re.compile(pat,  re.UNICODE)
WS_RE = mycompile(r' +')
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

	def generate_postid(self):
		rand = randint(0, 28922954)
		rand = 18779580
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
			
			f = open( str(postid)+'.txt', 'w' )
			for row in all: 
				content = strip_tags(row[0])+'\n'
				content = squeeze_whitespace(content)
				content = re.sub(r'\n ', '\n',content)
				content = re.sub(r'[\n]+', '\n',content)

				f.write(content)
			f.close()

	def read_post(self, post_id):
		db = MySQLdb.connect(host="localhost", 
		                     user="root", 
		                     passwd="ydh0114", 
		                     db="stackoverflow201503")
		cur = db.cursor() 
		cur.execute("SELECT Title FROM posts where Id=%s" % (post_id))
		title = cur.fetchall()

		cur.execute("SELECT Body FROM posts where Id=%s" %(post_id))
		body = cur.fetchall()
		cur.execute("SELECT Text FROM comments where PostId=%s" % (post_id))
		comments = cur.fetchall()

		if title[0][0] is None:
			all = body + comments
		else: 
			all = title + body + comments 

		f = open('out.txt', 'w')
		for row in all: 
			f.write(strip_tags(row[0])+'\n')
		f.close()

		return all



if __name__ ==  '__main__':
	r = DataReader()
	print r.generate_postid()