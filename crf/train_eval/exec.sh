#!/bin/sh
#crf_learn -f 2 -c 4.0 template train.data model
#crf_test -m model test.data  > crfresult1.txt
crf_learn -a MIRA -f 2 template train.data model
crf_test -m model test.data  > crfresult2.txt
rm -f model
