#!/bin/zsh
rm -r traindata_oct17
rm -r traindata_oct20
mkdir traindata_oct17
mkdir traindata_oct20

rm -rf oct17
rm -rf oct20

cp -r ~/brat/data/oct17 .
cp -r ~/brat/data/oct20 .

for p in cheeyong zhenchang ziqun deheng
do
	cd ./oct17/$p
	
	for f in *.txt
	do
		echo $f
		froot=`echo "$f" | cut -d'.' -f1`
		mv $f $f.bak
		cp ../../annotation-oct17/$p/$froot.txt.tk $f
		#python ~/sner/python/mytokenizer/mytokenizer.py $f $f.tk
		#mv $f.tk $f
		python ~/sner/python/anntoconll.py $f
	done

	cp *.conll ~/sner/python/traindata_oct17 

	cd ../..
done

for p in cheeyong liuyi ziqun deheng xuejiao chunyang gaosa lijing
do
	cd ./oct20/$p
	
	for f in *.txt
	do
		echo $f
		froot=`echo "$f" | cut -d'.' -f1`
		mv $f $f.bak
		cp ../../annotation-oct20/$p/$froot.txt.tk $f
		python ~/sner/python/anntoconll.py $f
	done

	cp *.conll ~/sner/python/traindata_oct20

	cd ../..
done

