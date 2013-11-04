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
    usage='''
Arguments: [file-dan-format]
Program to convert a file in Dan's format to sparse matrix format.
Outputs to stdout.
Example call: 
''' + sys.argv[0] + ''' /u/dhg/Corpora/nytgiga.lem.vc.f2000.m50.wInf.txt
'''
    sys.stderr.write(usage)

### main ###
a = datetime.now()

### 0. Process command line flags and arguments

argv = sys.argv[1:] # we exclude the name of the script
if len(argv) != 1:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(argv))+"\n")
    usage()
    sys.exit()

totransform = argv[0]

### 1. Main
totransformF = open(totransform,"r")
sys.stderr.write("Transforming file " + totransform + "\n")
for line in totransformF:
    elems = line.split("\n")[0].split("\t")
    word = elems.pop(0) # first item
    dims = range(0, len(elems), 2)
    for idim in dims:
        dim = elems[idim]
        if not dim == '':
            try:
                value = float(elems[idim+1])
            except ValueError:
                sys.stderr.write("Error! Not float: " + elems[idim+1])
            else:
                sys.stdout.write(word + " " + str(dim) + " " + str(value) + "\n")
totransformF.close()
sys.stderr.write("Done!\n")
