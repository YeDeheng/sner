To covert brat annotated ann and txt into conll format:
First, run my tokenizer on the annotated .txt file:
	-> python /path/to/mytokenizer.py a.txt a.txt.tk
Second, run anntoconll.py:
	-> python /path/to/anntoconll.py a.txt.tk 

All annotated files are under brat/data
