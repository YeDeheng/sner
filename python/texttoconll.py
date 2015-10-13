
# -*- coding: utf-8 -*-
import sys
import re
import os
from cStringIO import StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append('.')
from sentencesplit import sentencebreaks_to_newlines




def regex_or(*items):
  r = '|'.join(items)
  r = '(' + r + ')'
  return r
def pos_lookahead(r):
  return '(?=' + r + ')'
def optional(r):
  return '(%s)?' % r

PunctChars = r'''['“".?!,(/:;]'''
Entity = '&(amp|lt|gt|quot);'
# more complex version:
UrlStart1 = regex_or('https?://', r'www\.')
CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca','edu','gov')
UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$') # / added by Deheng

# Url = (r'\b' +
#     regex_or(UrlStart1, UrlStart2) +
#     UrlBody +
#     pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))
# print Url
#API = regex_or(r'((\w+)\.)+\w+\(\)', r'\w+\(\)', r'((\w+)\.)+(\w+)')
PunctSeq = r"""['`\"“”‘’)]+|[.?!,…]+|[:;/(]+"""
#API = r'((?:[a-zA-Z0-9]+\.)+[a-zA-Z0-9]+\(\)|[+$#0-9a-zA-Z\-]+|[^0-9a-zA-Z+$#\-])'
API = regex_or(r'(?:[a-zA-Z0-9]+\.)+[a-zA-Z0-9]+\(\)', r'[a-zA-Z0-9]+\(\)', r'(?:[a-zA-Z0-9]+\.)+[a-zA-Z0-9]+', r'\.[a-zA-Z]+', r'[a-z]+\'[a-z]+', r'[+$#0-9a-zA-Z_\-]+',  r'[^0-9a-zA-Z+$#_\-]', r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""")

TOKENIZATION_REGEX = re.compile(API)
NEWLINE_TERM_REGEX = re.compile(r'(.*?\n)')

def text_to_conll(f):
    """Convert plain text into CoNLL format."""
    sentences = []
    for l in f:
        l = sentencebreaks_to_newlines(l)
        sentences.extend([s for s in NEWLINE_TERM_REGEX.split(l) if s])

    lines = []
    for s in sentences:
    	print s
        nonspace_token_seen = False
        print TOKENIZATION_REGEX.split(s)
        tokens = [t for t in TOKENIZATION_REGEX.split(s) if t]
        for t in tokens:
            if not t.isspace():
                lines.append([t, 'O'])
                nonspace_token_seen = True
        # sentences delimited by empty lines
        if nonspace_token_seen:
            lines.append([])

    lines = [[l[0], l[1]] if l else l for l in lines]
    return StringIO('\n'.join(('\t'.join(l) for l in lines)))

if __name__ == '__main__':
	f = open('example.txt', 'r')
	lines = text_to_conll(f)
	with open('out.txt', 'wt') as of:
		of.write(''.join(lines))