#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

# program to extract content words from the malt-parsed corpora (bnc, wikipedia, ukwac)
# created gbt, Oct 2012

### import
import sys
from datetime import datetime
from procmalt import Sentence, Node, token_type
import math
import gzip
import os
import re
import getopt

### functions ###

def printContentWord(n):
    '''Print lemma of a node, if it is an adjective, noun, non-auxiliary verb, or adverb'''
    global _debug
    aux = ''
    regex = re.compile(  '^[a-zA-Z]+([\-][a-zA-Z]+)*(\')?$')
    if regex.match(n.lemma):
        firsttwo = n.POS[:2]
        firstone = n.POS[0]
        if firsttwo == 'JJ':
            aux = n.lemma
        elif firstone == 'N':
            aux = n.lemma
        elif firsttwo == 'VV':
            aux = n.lemma
        elif firsttwo == 'RB':
            aux = n.lemma

    if not aux == '':
        sys.stdout.write(aux + "\n")

def printContentWordWithPOS(n):
    '''Print lemma-pos of a node, if it is an adjective, common noun, non auxiliary verb, or adverb'''
    global _debug
    aux = ''
    regex = re.compile(  '^[a-zA-Z]+([\-][a-zA-Z]+)*(\')?$')
    if regex.match(n.lemma):
        firsttwo = n.POS[:2]
        if firsttwo == 'JJ':
            aux = n.lemma + "-j"
        elif firsttwo == 'NN':
            aux = n.lemma + "-n"
        elif firsttwo == 'VV':
            aux = n.lemma + "-v"
        elif firsttwo == 'RB':
            aux = n.lemma + "-r"

    if not aux == '':
        sys.stdout.write(aux + "\n")

def process(c):
    '''read corpus and output each occ of a content word'''
    global _debug
    global _lemmaonly
    f = gzip.open(c)
    i = 0
    for line in f:
        i = i + 1
        if i%1000000 == 0:
            sys.stderr.write("line: " + str(i) + " of corpus " + c +"\n")
        if token_type(line) == "word":
            try:
                node = Node(inputl=line)
            except RuntimeError, err:
                sys.stderr.write(str(err))
            else:
                if _lemmaonly: printContentWord(node)
                else: printContentWordWithPOS(node)

        elif token_type(line) == False:
            sys.stderr.write("* Reached EOF *\n")

### main ###
a = datetime.now()

def usage():
    usage='''
Program to extract a list of content words from a malt-parsed corpus.
Usage:
Arguments: [corpus-dir]
Options: -l, --lemmaonly: only lemma (default: lemma-shortpos, as in can-n, can-v, small-j).
Processes all gz files in corpus-dir.
Output: stdout, each content word occurrence, one per line.
Messages: stderr.
Example call:
python '''  + sys.argv[0] + ''' -l /scratch/cluster/gboleda/corpora/
'''
    sys.stderr.write(usage)

### 0. Process command line arguments

_debug = 0
_lemmaonly = False
argv = sys.argv[1:] # we exclude the name of the script
try:
    opts, args = getopt.getopt(argv, "hld", ["help", "lemmaonly","debug"])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ('-d', '--debug'):
        _debug = 1
    elif opt in ('-l', '--lemmaonly'):
        _lemmaonly = True
    else:
        sys.stderr.write("Error: unrecognized option: " + str(opt) + "\n")
        usage()
        sys.exit()

if len(args) != 1:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(args))+"\n")
    sys.stderr.write("Arguments: " + str(args))
    usage()
    sys.exit()

corpusDir = args[0]
#"/scratch/cluster/gboleda/corpora/"
#/mnt/cimec-storage-sata/users/marco.baroni/share/ukwac-maltparsing/data/"

for corpusfile in os.listdir(corpusDir):
     if corpusfile.endswith(".gz"):
         s = os.path.join(corpusDir, corpusfile)
         sys.stderr.write("Processing file " + s + "\n")
         process(s)
# s="code/bnc.tiny.gz"
# sys.stderr.write("Processing file " + s + "\n")
# process(s)

b = datetime.now()
c = b - a
sys.stderr.write("Time spent (hours):" + str(c.seconds/3600) + "\n")
