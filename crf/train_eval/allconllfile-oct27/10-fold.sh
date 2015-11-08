#!/bin/zsh
rm part*

for i in {0..9}
do
	touch part$i
done

m=0
for f in ./*.conll*-doc-*.conll
do
	cnt=$((m%10))
	for i in {0..9}
	do
		if [ $cnt -eq $i ]; then
			cat $f >> part$i
			echo >> part$i
		fi
	done
	m=`expr $m + 1`
done

for i in {0..9}
do
	rm train$i.tmp
	rm test$i.tmp
done

for i in {0..9}
do
	touch train$i.tmp
	touch test$i.tmp
done

j=9
for k in {0..9}
do
	for i in {0..9}
	do
		if [ $i != $j ]; then
			cat part$i >> train$k.tmp
		else
			cat part$i >> test$k.tmp
		fi
	done
	j=`expr $j - 1`
done

for i in {0..9}
do
	python ../converttorawconll.py train$i.tmp train$i.conll
	python ../converttorawconll.py test$i.tmp test$i.conll
done


for i in {0..9}
do
	mv train$i.conll train$i.bakup
	python urlrep.py train$i.bakup train$i.conll
	mv test$i.conll test$i.bakup
	python urlrep.py test$i.bakup test$i.conll
done

sed -i "s/@codeSnippetRemoved/@c@/g" train*.conll
sed -i "s/@codeSnippetRemoved/@c@/g" test*.conll

cd ../../
for i in {0..9}
do
	python featureextractor.py ./train_eval/allconllfile-oct27/train$i.conll ./train_eval/train$i.data
	python featureextractor.py ./train_eval/allconllfile-oct27/test$i.conll ./train_eval/test$i.data
done
cd ./train_eval/allconllfile-oct27
