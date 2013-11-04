#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

# created gbt, Nov 2012

### import
import sys
from datetime import datetime
import math
import gzip
import os
import getopt
import re

### functions ###

def usage():#
#\tOptionally accepts -d or --debug flag (verbose output), -h or --help flags.
    usage='''
Arguments: [file-to-clean] [file-with-elements-to-select]
Program to select lines of a tab-separated file file (arg1) whose second field coincides with the first field of a second file (arg2).
Outputs to stdout.
Example call: 
''' + sys.argv[0] + ''' ../data/counts/coocs.ans.peripheral.notrevised ../data/dataset/test.ans
'''

# test:
# removed ANs:
# Aboriginal-j_people-n
# African-j_community-n

    sys.stderr.write(usage)

def loadFile(f,s):
    elemF = open(f,"r")
    for line in elemF.readlines():
        word = line.split("\n")[0].split("\t")[0]
        # if _debug == 1: print(word)
        s.add(word)
        elemF.close()
    sys.stderr.write("Elem file " + f + " loaded\n")
    return s

### main ###
a = datetime.now()

### 0. Process command line flags and arguments

argv = sys.argv[1:] # we exclude the name of the script
if len(argv) != 2:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(argv))+"\n")
    usage()
    sys.exit()

toclean = argv[0]
elems = argv[1]

### 1. Load element files

elemSetEmpty = set()
elemSet = loadFile(elems,elemSetEmpty)
sys.stderr.write("Pool of elements that will be selected, if present in the input file: " + str(len(elemSet)) + "\n")

### 2. Clean file
#tocleanF = open(toclean,"r")
tocleanF = gzip.open(toclean,"r")
#elem = False
sys.stderr.write("Cleaning file " + toclean + "\n")
for line in tocleanF:
    elem = line.split("\n")[0].split("\t")[1]
#    print(elem)
#    print(elist)
    if elem in elemSet:
        sys.stdout.write(line)
tocleanF.close()
sys.stderr.write("Done!\n")
