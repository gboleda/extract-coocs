#!/bin/bash -l
# script to gather coocs for wikipedia, ukwac, and bnc corpora
# gbt, Oct 28th 2012
#$ -wd /mnt/cimec-storage-sas/home/gemma.boledatorrent/share
#$ -S /bin/bash
#$ -j y
#$ -m bea
#$ -M gemma.boleda@unitn.it

#for corpus in bnc wikipedia-1 wikipedia-2 wikipedia-3 wikipedia-4 ukwac1 ukwac2 ukwac3 ukwac4 ukwac5

export LC_ALL=C
DIR='data/counts'

echo "begin"

date

mkdir tmp2
/opt/python/bin/python2.7 code/extract-coocs.py /mnt/cimec-storage-sata/users/marco.baroni/share/ukwac-maltparsing/data $DIR/targets.4Kj.8Kn $DIR/dims-with-freq.10300 | sort -T tmp2 |uniq -c| gawk '{print $2 "\t" $3 "\t" $1}' > $DIR/coocs.n.j

date

echo "done"
