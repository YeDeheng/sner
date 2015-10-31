#!/bin/zsh

for i in {0..9}
do
	perl conlleval.pl -d "\t" < crfresult$i
done

