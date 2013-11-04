export LC_ALL=C

scratch='/scratch/cluster/gboleda'
out="$scratch/counts/bnc-ukwac-wacky.all.content.words.lemmaonly"

echo "begin"
date

mkdir $scratch/tmp3
mkdir $scratch/tmp2
rm -f $scratch/tmp3/*
rm -f $scratch/tmp2/*
python /u/gboleda/code/extract-content-words.py -l $scratch/corpora | sort -T $scratch/tmp3 | uniq -c | sort -rgT $scratch/tmp2 | gawk '{print $2 "\t" $1}' > $out

rm -f $scratch/tmp3/*
rm -f $scratch/tmp2/*
# test
#python /u/gboleda/code/extract-content-words.py -l /u/gboleda/code/test | sort -T /scratch/cluster/gboleda/tmp3 | uniq -c | sort -rgT /scratch/cluster/gboleda/tmp2 | gawk '{print $2 "\t" $1}' > /scratch/cluster/gboleda/counts/test

date
echo "done"
