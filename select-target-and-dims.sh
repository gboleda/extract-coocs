#!/bin/bash -l

export LC_ALL=C

DIR='/mnt/cimec-storage-sas/home/gemma.boledatorrent/share'

chmod u+w $DIR/data/counts/targets.4Kj.8Kn
chmod u+w $DIR/data/counts/dims-with-freq.10300
grep -P '\-n\t' $DIR/data/counts/all.content.words |head -8000 | gawk '{print $1}' > $DIR/data/counts/target.nouns.8K
grep -P '\-j\t' $DIR/data/counts/all.content.words |head -4000 | gawk '{print $1}' > $DIR/data/counts/target.adjs.4K
cat $DIR/data/counts/target.adjs.4K $DIR/data/counts/target.nouns.8K | sort > $DIR/data/counts/targets.4Kj.8Kn.toclean
# we prune the target elements
$DIR/code/remove-problematic-words.py $DIR/data/counts/targets.4Kj.8Kn.toclean $DIR/data/misc/adjs-to-prune.txt $DIR/data/misc/nouns-to-prune.txt > $DIR/data/counts/targets.4Kj.8Kn
rm -f $DIR/data/counts/target.adjs.4K $DIR/data/counts/target.nouns.8K $DIR/data/counts/targets.4Kj.8Kn.toclean
head -10300 $DIR/data/counts/all.content.words > $DIR/data/counts/dims-with-freq.10300
chmod u-w $DIR/data/counts/targets.4Kj.8Kn
chmod u-w $DIR/data/counts/dims-with-freq.10300
