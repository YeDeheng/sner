import sys
import re
import os
from cStringIO import StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append('.')
from sentencesplit import sentencebreaks_to_newlines


TOKENIZATION_REGEX = re.compile(r'([0-9a-zA-Z]+|[^0-9a-zA-Z])')
NEWLINE_TERM_REGEX = re.compile(r'(.*?\n)')

def text_to_conll(f):
    """Convert plain text into CoNLL format."""
    sentences = []
    for l in f:
        l = sentencebreaks_to_newlines(l)
        sentences.extend([s for s in NEWLINE_TERM_REGEX.split(l) if s])

    # lines = []

    # offset = 0
    # for s in sentences:
    #     nonspace_token_seen = False

    #     tokens = [t for t in TOKENIZATION_REGEX.split(s) if t]

    #     for t in tokens:
    #         if not t.isspace():
    #             lines.append(['O', offset, offset+len(t), t])
    #             nonspace_token_seen = True
    #         offset += len(t)

    #     # sentences delimited by empty lines
    #     if nonspace_token_seen:
    #         lines.append([])

    # # add labels (other than 'O') from standoff annotation if specified
    # if options.annsuffix:
    #     lines = relabel(lines, get_annotations(f.name))

    # lines = [[l[0], str(l[1]), str(l[2]), l[3]] if l else l for l in lines]
    # return StringIO('\n'.join(('\t'.join(l) for l in lines)))


if __name__ == '__main__':
	text_to_conll('example.txt')