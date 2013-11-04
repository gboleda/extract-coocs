#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

# program to get rid of problematic words in data extracted from
# the malt-parsed bnc, ukwac, wackypedia corpora
# Takes file as input, outputs to stdout.
# created gbt, Nov 2012

### import
import sys
from datetime import datetime
import math
#import gzip
import os
import getopt
import re

### functions ###

def usage():#
#\tOptionally accepts -d or --debug flag (verbose output), -h or --help flags.
    usage='''
# program to get rid of problematic words in data extracted from
# the malt-parsed bnc, ukwac, wackypedia corpora
# Takes file, two lists of problematic elements as input, outputs to stdout.
Example call: python ''' + sys.argv[0] + " ../data/counts/targets.4Kj.4Kn"

    sys.stderr.write(usage)

def loadFile(f,s):
    problF = open(f,"r")
    for line in problF.readlines():
        word = line.split("\n")[0].split("\t")[0]
    # if _debug == 1: print(word)
        s.add(word)
        problF.close()
    sys.stderr.write("Probl file " + f + " loaded\n")
    return s

### main ###
a = datetime.now()

### 0. Process command line flags and arguments

argv = sys.argv[1:] # we exclude the name of the script
if len(argv) != 3:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(argv))+"\n")
    usage()
    sys.exit()

toclean = argv[0]
probl1 = argv[1]
probl2 = argv[2]

### 1. Load problematic files

problSet = set()
problSet1 = loadFile(probl1,problSet)
problSet = loadFile(probl2,problSet1)
sys.stderr.write("Number of problematic elements: " + str(len(problSet)) + "\n")

### 2. Clean file
tocleanF = open(toclean,"r")
problem = False
sys.stderr.write("Cleaning file " + toclean + "\n")
for line in tocleanF.readlines():
    elem = line.split("\n")[0].split("\t")[0]
    # if _debug == 1: print(word)
#    print(elem)
    elist = elem.split('_')
#    print(elist)
    for e in elist:
        if e in problSet:
            problem = True
            #print("\tis problematic: "+e)
    if problem == False:
        sys.stdout.write(line)
    problem = False
tocleanF.close()
sys.stderr.write("Done!\n")
