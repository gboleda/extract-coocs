#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

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
Arguments: [file-to-clean] [file-with-elements-to-select-or-remove]
Program to select lines of a file (arg1) that coincide with the lines of a second file (arg2).
Outputs to stdout.
Example call: 
python ''' + sys.argv[0] + ''' ../data/counts/ans.peripheral.notrevised ../data/dataset/ans.test
'''

# test:
# removed ANs:
# Aboriginal-j_people-n
# African-j_community-n

    sys.stderr.write(usage)

def loadFile(f,s):
    elemF = open(f,"r")
    for line in elemF.readlines():
    # if _debug == 1: print(word)
        s.add(line)
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
sys.stderr.write("Number of elements: " + str(len(elemSet)) + "\n")

### 2. Clean file
tocleanF = open(toclean,"r")
#elem = False
sys.stderr.write("Cleaning file " + toclean + "\n")
for line in tocleanF.readlines():
    # if _debug == 1: print(word)
#    print(elem)
    if line in elemSet:
        sys.stdout.write(line)
#    else:
#        print("NO: "+line)
tocleanF.close()
sys.stderr.write("Done!\n")
