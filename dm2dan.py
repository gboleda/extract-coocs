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
Arguments: [file-dm-format]
Program to conver a file in dense matrix (dm) format to Dan's format. Uses dummy dimension names.
Outputs to stdout.
Example call: 
''' + sys.argv[0] + ''' /u/gboleda/resources/CORE_SS.CORE_SS.bnc-ukwac-wacky.min50.10K.ppmi.svd_500.dm
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
    sys.stdout.write(word)
    dims = range(0, len(elems))
    for idim in dims:
        dimlabel = 'd'+str(idim)
        dim = elems[idim]
        if not dim == '':
            try:
                value = float(dim)
            except ValueError:
                sys.stderr.write("Error! Not float: " + str(dim))
            else:
                sys.stdout.write("\t" + dimlabel + "\t" + str(value))
    sys.stdout.write("\n")
totransformF.close()
sys.stderr.write("Done!\n")
