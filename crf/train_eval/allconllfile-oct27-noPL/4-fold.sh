#!/bin/zsh
i=0
rm part*
touch part1
touch part2
touch part3
touch part4

for f in ./*.conll*-doc-*.conll
do
	cnt=$((i%4))
	
	if [ $cnt -eq 0 ]; then
		cat $f >> part1
		echo >> part1
	fi

	if [ $cnt -eq 1 ]; then
		cat $f >> part2
		echo >> part2
	fi

	if [ $cnt -eq 2 ]; then
		cat $f >> part3
		echo >> part3
	fi

	if [ $cnt -eq 3 ]; then
		cat $f >> part4
		echo >> part4
	fi

	i=`expr $i + 1`
done

for i in 1 2 3 4
do
	rm train$i.tmp
	rm test$i.tmp
done

for i in 1 2 3 4
do
	touch train$i.tmp
	touch test$i.tmp
done

cat part1 >> train1.tmp
cat part2 >> train1.tmp
cat part3 >> train1.tmp
cat part4 >> test1.tmp

cat part1 >> train2.tmp
cat part2 >> train2.tmp
cat part3 >> test2.tmp
cat part4 >> train2.tmp

cat part1 >> train3.tmp
cat part2 >> test3.tmp
cat part3 >> train3.tmp
cat part4 >> train3.tmp

cat part1 >> test4.tmp
cat part2 >> train4.tmp
cat part3 >> train4.tmp
cat part4 >> train4.tmp

for i in 1 2 3 4
do
	python ../converttorawconll.py train$i.tmp train$i.conll
	python ../converttorawconll.py test$i.tmp test$i.conll
done

cd ../../
for i in 1 2 3 4
do
	python featureextractor.py ./train_eval/allconllfile-oct27/train$i.conll ./train_eval/train$i.data
	python featureextractor.py ./train_eval/allconllfile-oct27/test$i.conll ./train_eval/test$i.data
done
cd ./train_eval/allconllfile-oct27
