#!/bin/zsh
i=0
rm train.tmp
rm test.tmp
touch train.tmp
touch test.tmp

for f in ./*.conll
do
	cnt=$((i%2))
	
	if [ $cnt -eq 0 ]; then
		cat $f >> train.tmp
		echo >> train.tmp
	fi

	if [ $cnt -eq 1 ]; then
		cat $f >> test.tmp
		echo >> test.tmp
	fi

	i=`expr $i + 1`
done
