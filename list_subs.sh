#!/bin/bash
# 
# write a text file with a list of names
#
# e.g. ./list_subs.sh 50 60 subs.txt 'P' will produce a file subs.txt with P50, P51, P52...P60
#
# If file already exists, calling list_subs.sh will overwrite anything that's there
#

> $3

min=$1;
max=$2;
while [ "$min" -le "$max" ]; do
	echo "$4$min" >> $3
	min=`expr "$min" + 1`;
done
