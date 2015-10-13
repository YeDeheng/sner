
# -*- coding: utf-8 -*-
import sys
import re
import os
from cStringIO import StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append('.')
from sentencesplit import sentencebreaks_to_newlines

PLs = ['java', 
       'javascript', 
       'c#', 
       'php', 
       'python', 
       'html', 
       'c++' ] 
Plats = ['android', 'ios']
Frams = ['jquery']


def regex_or(*items):
  r = '|'.join(items)
  r = '(' + r + ')'
  return r
# def pos_lookahead(r):
#   return '(?=' + r + ')'
# def optional(r):
#   return '(%s)?' % r

# PunctChars = r'''['“".?!,(/:;]'''
# Entity = '&(amp|lt|gt|quot);'
# # more complex version:
# UrlStart1 = regex_or('https?://', r'www\.')
# CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca','edu','gov')
# UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
# UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
# UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
# UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$') # / added by Deheng

API_pattern = re.compile(regex_or(r'^(?:[a-zA-Z0-9]+\.)+[a-zA-Z0-9]+\(\)$', 
    r'^[a-zA-Z0-9]+\(\)$', 
    r'^(?:[a-zA-Z0-9]+\.)+[a-zA-Z0-9]+$', 
    r'^[A-Z][a-z]+[A-Z][a-z]+$' ))
    # r'^\.[a-zA-Z]+$',  # this can be .net 
    # r'^[a-z]+\'[a-z]+$',  # not sure why I added this
    # r'^[+$#0-9a-zA-Z_\-]+$',  
    # r'^[^0-9a-zA-Z+$#_\-]$' ))

# TOKENIZATION_REGEX = re.compile(API)
NEWLINE_TERM_REGEX = re.compile(r'(.*?\n)')

def text_to_conll(f, top_tag):
    """Convert plain text into CoNLL format."""
    sentences = []
    for l in f:
        l = sentencebreaks_to_newlines(l)
        sentences.extend([s for s in NEWLINE_TERM_REGEX.split(l) if s])

    lines = []
    for s in sentences:
        nonspace_token_seen = False
        tokens = [t for t in s.split() if t]
        for t in tokens:
            if not t.isspace():
                # pre label rules designed by Deheng
                if t.lower() in PLs:
                    lines.append([t, 'B-PL'])
                elif t.lower() in Plats:
                    lines.append([t, 'B-Plat'])
                elif t.lower() in Frams:
                    lines.append([t, 'B-Fram'])
                elif API_pattern.match(t) is not None:
                    lines.append([t, 'B-API'])
                else:
                    lines.append([t, 'O'])
                nonspace_token_seen = True
        # sentences delimited by empty lines
        if nonspace_token_seen:
            lines.append([])

    lines = [[l[0], l[1]] if l else l for l in lines]
    return StringIO('\n'.join(('\t'.join(l) for l in lines)))

def main(arg1, arg2):
    f = open(arg1, 'r')
    top_tag = re.split(r'[0-9]+', arg1)[0]
    lines = text_to_conll(f, top_tag)
    with open(arg2, 'wt') as of:
        of.write(''.join(lines))

if __name__ == '__main__':
    main(*sys.argv[1:])

