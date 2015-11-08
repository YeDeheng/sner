# -*- coding: utf-8 -*-

import re,sys

def regex_or(*items):
  r = '|'.join(items)
  r = '(' + r + ')'
  return r
def pos_lookahead(r):
  return '(?=' + r + ')'
def optional(r):
  return '(%s)?' % r

def urlrep(word):
  PunctChars = r'''['“".?!,(/:;]'''
  Entity = '&(amp|lt|gt|quot);'
  UrlStart1 = regex_or('https?://', r'www\.')
  CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca','edu','gov')
  UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
  UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
  UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
  UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$') # / added by Deheng
  Url = (r'\b' +
  regex_or(UrlStart1, UrlStart2) + UrlBody + pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))
  Url_RE = re.compile("(%s)" % Url, re.U|re.I)
  return Url_RE.sub("@u@", word)

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')
for line in f1:
  f2.write(urlrep(line))
f1.close()
f2.close()
