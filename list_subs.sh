#!/bin/bash
# 
# write a text file with a list of names
#

> subs.txt

min=$1;
max=$2;
while [ "$min" -le "$max" ]; do
	echo "P$min" >> subs.txt
	min=`expr "$min" + 1`;
done
