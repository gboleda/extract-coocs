#!/bin/bash -l
#$ -wd /mnt/cimec-storage-sas/home/gemma.boledatorrent/share
#$ -S /bin/bash
#$ -j y
#$ -m bea
#$ -M gemma.boleda@unitn.it

export LC_ALL=C

echo "begin"
date

mkdir tmp1
/opt/python/bin/python2.7 code/extract-ans.py /mnt/cimec-storage-sata/users/marco.baroni/share/ukwac-maltparsing/data data/counts/targets.4Kj.8Kn | sort -T tmp1 | uniq -c | sort -rgT tmp1 | gawk '{print $2 "\t" $1}' > data/counts/all.ans.4Kj.8Kn

date
echo "done"
