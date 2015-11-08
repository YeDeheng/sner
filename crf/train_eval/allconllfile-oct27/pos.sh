#!/bin/zsh
cd ../../
for i in {0..9}
do
	python featureextractor-pos.py ./train_eval/allconllfile-oct27/train$i.conll.pos ./train_eval/train$i.data
	python featureextractor-pos.py ./train_eval/allconllfile-oct27/test$i.conll.pos ./train_eval/test$i.data
done
cd ./train_eval/allconllfile-oct27
