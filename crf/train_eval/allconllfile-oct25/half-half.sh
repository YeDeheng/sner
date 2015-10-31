#!/bin/zsh
i=0
mkdir train-set
mkdir test-set
for f in ./*.conll
do
	cnt=$((i%2))
	
	if [ $cnt -eq 0 ]; then
		cp $f ./train-set
		cat $f >> train.conll
		echo >> train.conll
	fi

	if [ $cnt -eq 1 ]; then
		cp $f ./test-set
		cat $f >> test.conll
		echo >> test.conll
	fi

	i=`expr $i + 1`
done
